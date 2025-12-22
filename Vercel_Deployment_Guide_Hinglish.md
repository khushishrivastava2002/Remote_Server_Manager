# Vercel Deployment Guide (Hinglish)

Ab kyunki aapka code GitHub par hai aur database Atlas se connected hai, Vercel par deploy karna bohot aasaan hai.

## Steps:

1.  **Vercel par Login karein:**

    - [https://vercel.com](https://vercel.com) par jayein.
    - **"Continue with GitHub"** select karein.

2.  **New Project Import karein:**

    - Dashboard par **"Add New..."** -> **"Project"** par click karein.
    - Aapko apni GitHub repositories dikhengi.
    - **`Remote_Server_Manager`** ke bagal mein **"Import"** button dabayein.

3.  **Project Configure karein:**

    - **Framework Preset:** Ise **"Other"** hi rehne dein (kyunki humne `vercel.json` banaya hai, Vercel khud samajh jayega).
    - **Root Directory:** `./` (Default) rehne dein.
    - **Environment Variables:** Filhal humne database URL code mein hi daal diya hai, to yahan kuch karne ki zarurat nahi hai. (Future mein aap secrets yahan daal sakte hain).

4.  **Deploy:**

    - Niche **"Deploy"** button par click karein.
    - Thodi der wait karein (Building... dikhayega).

5.  **Success!**

    - Jab deploy ho jayega, to aapko confetti (patakhe) dikhenge 🎉.
    - **"Continue to Dashboard"** par click karein.
    - Wahan **"Domains"** section mein aapko apne app ka live URL mil jayega (e.g., `remote-server-manager.vercel.app`).

6.  **Test karein:**
    - Us URL ko open karein aur aage `/docs` lagayein (e.g., `https://your-app.vercel.app/docs`).
    - Agar Swagger UI khul gaya, to aapka app live hai!
