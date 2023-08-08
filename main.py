import customtkinter
import re
import requests
from bs4 import BeautifulSoup

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x500")

frame = customtkinter.CTkFrame(master=root)
frame.pack(fill="both", expand=True)

label = customtkinter.CTkLabel(
    master=frame, text="Welcome", font=("Roboto", 24))
label.pack(pady=12, padx=10)


def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)
    global statement
    statement = choice


def print_textbox_content():

    permittext = permit.get()
    monthtext = month.get()
    daytext = day.get()
    yeartext = yr.get()

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.schedule2drive.com/index.php")
        page.fill('input#inputLoginPermit', permittext)
        page.fill('input#inputLoginMonth', monthtext)
        page.fill('input#inputLoginDay', daytext)
        page.fill('input#inputLoginYear', yeartext)

        select_element = page.locator('select#inputLoginState')

    # Select an option by its value

        select_element.select_option(value=statement)
        page.click('button[type = button]')
        page.wait_for_selector('a:has-text("Schedule Drives")')

        page.click('a:has-text("Schedule Drives")')

        html = page.inner_html('#box')
        page.is_visible('boxMiddle_greenGreen')
        soup = BeautifulSoup(html, 'html.parser')

    td_elements = soup.find_all("td", class_="day")
    for td_element in td_elements:

        full_div_element = td_element.find("div", class_="full")

        if full_div_element is None:
            continue

        print("Full div element found")

        date_div_element = full_div_element.find_parent(
            "td").find("div", class_="date")

        if date_div_element is None:
            print("Date div element not found")
            continue
        print("Date div element found")

        dateElement = (date_div_element.text).strip()
        print(f'There are full days on {dateElement}.')

    open_slot_links = soup.find_all("a", text="Open Slots")

    for link in open_slot_links:
        href = link["href"]
        match = re.search(r"\bdate=([0-9-]+)\b", href)
        if match:
            date = match.group(1)
            open = customtkinter.CTkLabel(
                master=frame, text=f"Found open slot on date: {date}", font=("Roboto", 10), text_color="green")
            open.pack(pady=0, padx=10)

            print(f"Found open slot on date: {date}")
        else:
            print("No date found")
            close = customtkinter.CTkLabel(
                master=frame, text="No dates found 😔", font=("Roboto", 10))
            close.pack(pady=0, padx=10)


permit = customtkinter.CTkEntry(master=frame, placeholder_text="Permit ID")
permit.pack(pady=12, padx=10)


b = customtkinter.CTkFrame(master=frame)
b.pack()  # Use pack() for the 'b' frame
bday_frame = customtkinter.CTkFrame(master=b)
bday_frame.grid(row=0, column=1, padx=10, pady=12)

month = customtkinter.CTkEntry(master=bday_frame, width=30)
month.grid(row=0, column=0, padx=10)

day = customtkinter.CTkEntry(master=bday_frame, width=30)
day.grid(row=0, column=1, padx=10)

yr = customtkinter.CTkEntry(master=bday_frame, width=30)
yr.grid(row=0, column=2, padx=10)

bdaytext = customtkinter.CTkLabel(
    master=frame, text="Birthday(MM/DD/YYYY)", font=("Roboto", 10))
bdaytext.pack(pady=0, padx=10)


combobox = customtkinter.CTkComboBox(master=frame, values=["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                                                           "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                                                           "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                                                           "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                                                           "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"],
                                     command=combobox_callback
                                     )


combobox.set("Pick State")

print(combobox.get())

combobox.pack(pady=12, padx=10)

button = customtkinter.CTkButton(
    master=frame, text="Find Open Slots", command=print_textbox_content)
button.pack(pady=17, padx=10)


root.mainloop()
