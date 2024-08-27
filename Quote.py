import requests
import sqlite3

connection = sqlite3.connect('quote.db')
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS quotes')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotes (
               id INTEGER PRIMARY KEY,
               content TEXT NOT NULL,
               author TEXT NOT NULL
               )
''')

def save_quote(content, author):
    cursor.execute("INSERT INTO quotes (content, author) VALUES (?, ?)", (content, author))
    connection.commit()

def fetch_quote():
    url = "https://api.freeapi.app/api/v1/public/quotes/quote/random"
    response = requests.get(url)
    data = response.json()

    if data["success"] and "data" in data:
        author = data["data"]["author"]
        content = data["data"]["content"]
        return content, author
    else:
        raise Exception("Failed to fetch quote")

def list_all_quotes():
    cursor.execute("SELECT * FROM quotes")
    for row in cursor.fetchall():
        print(row)

def delete_quote(quote_id):
        cursor.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))
        connection.commit()
        print("Post deleted❌ successfully.")

def main():
    while True:
        print("*" * 70)
        print("Quotes with Writer")
        print("1: Get a Quote")
        print("2: Show all the saved Quotes")
        print("3: Delete any saved Quote")
        print("4: Exit APP")
        choice = input("Enter your choice: ")
        if choice == '1':
            try:
                content, author = fetch_quote()
                print(f"{content} : {author}")
                save = input("Do you want to save this post: Yes📌, No❌: ")
                savepost = save.lower()
                if savepost == "yes":
                    save_quote(content, author)
                    print("Post saved successfully.✔️")
            except Exception as e:
                print(str(e))
        elif choice == '2':
            print("*" * 70)
            list_all_quotes()
        elif choice == '3':
                quote_id = int(input("Enter quote id to delete[❌]: "))
                delete_quote(quote_id)
        elif choice == '4':
            break
        else:
            print("Invalid Choice!")
    connection.close()

if __name__ == "__main__":
    main()
