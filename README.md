# 📋 CS50W Project 2 - Commerce 

## ✅ Requirements

### 1. Models

- Your application must include **at least three models** in addition to the built-in `User` model:
  - **Auction Listings**
  - **Bids**
  - **Comments**
- You're free to define what fields each model should have and their types.
- You may add additional models if necessary.

---

### 2. Create Listing

- Users should be able to **create new auction listings**.
- The listing form should allow users to provide:
  - Title (required)
  - Description (text-based, required)
  - Starting bid (required)
  - Image URL (optional)
  - Category (optional, e.g., *Fashion*, *Toys*, *Electronics*, *Home*)

---

### 3. Active Listings Page

- The default route (`/`) should display **all currently active auction listings**.
- For each listing, display at minimum:
  - Title
  - Description
  - Current price
  - Image (if provided)

---

### 4. Listing Page

- Clicking a listing should go to a **dedicated page** with all the listing details.

#### Features for Signed-In Users:

- ✅ Add or remove the listing from a **Watchlist**.
- ✅ Place a **bid**:
  - Must be at least the starting bid.
  - Must be higher than any existing bids.
  - Show an error if bid is invalid.
- ✅ If the user **created the listing**, they can **close the auction**:
  - The highest bidder becomes the winner.
  - The listing becomes inactive.
- ✅ If the user **won a closed auction**, show a message indicating they won.
- ✅ Users can **add comments** to the listing.
- ✅ Display all comments under the listing.

---

### 5. Watchlist

- Signed-in users should have access to a **Watchlist page**.
- This page displays all listings the user has added to their watchlist.
- Clicking a listing takes the user to the listing page.

---

### 6. Categories

- Provide a page that lists all **available listing categories**.
- Clicking a category shows all **active listings** in that category.

---

### 7. Django Admin Interface

- Using Django’s built-in admin:
  - Site administrators should be able to **view, add, edit, and delete** any:
    - Listings
    - Comments
    - Bids

---

## 💡 Hints

- Create a superuser account using:
  ```bash
  python manage.py createsuperuser

