# MongoDB Atlas Setup Guide (Hinglish)

MongoDB Atlas par free database banane ke liye ye steps follow karein:

## 1. Account Create Karein

- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) par jayein.
- Google se sign up kar lein (sabse aasaan hai).

## 2. Cluster Banayein

- Login karne ke baad, **"Build a Database"** par click karein.
- **M0 Free** plan select karein.
- Provider (AWS) aur Region (jo bhi default ho, ya India ke paas wala) select karein.
- Niche **"Create"** button dabayein.

## 3. User Create Karein

- Aapko **"Security Quickstart"** dikhega.
- **Username** aur **Password** set karein (Password yaad rakhein, ye baad mein chahiye hoga).
- **"Create User"** par click karein.

## 4. IP Access Allow Karein

- Usi page par niche **"Network Access"** hoga.
- **"Allow Access from Anywhere"** (0.0.0.0/0) select karein. (Ye zaroori hai taaki Vercel/Render connect kar sake).
- **"Add IP Address"** par click karein.
- Fir **"Finish and Close"** dabayein.

## 5. Connection String Lein

- Ab aap apne Dashboard par honge.
- Apne Cluster ke paas **"Connect"** button par click karein.
- **"Drivers"** option select karein.
- Aapko ek URL dikhega, kuch aisa:
  `mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority`
- Is URL ko copy kar lein.

## 6. Code Update Karein

- Is URL mein `<password>` ki jagah apna step 3 wala password dalein.
- Ab is poore URL ko `app/database.py` mein `MONGODB_URL` ki jagah paste karein.
  - **Note:** Security ke liye behtar hoga ki aap ise code mein hardcode na karein, balki Vercel/Render ke **Environment Variables** mein set karein.
