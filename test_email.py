from simplegmail import Gmail
# No circular import now!

def test_connection():
    try:
        gmail = Gmail()
        print("Successfully connected to Gmail!")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()