# SSH Command Execution Kaise Kaam Karta Hai?

Humne `app/routers/servers.py` file mein SSH command execution ka logic implement kiya hai. Yahan step-by-step explanation hai ki ye kaise achieve kiya gaya hai:

## 1. Endpoint Setup

Humne ek API endpoint banaya hai: `POST /servers/{server_id}/execute`.
Jab aap is URL par request bhejte hain, to aapko `server_id` (jis server par command chalana hai) aur `command` (kya chalana hai) dena hota hai.

## 2. Safety Check (Suraksha Jaanch)

Sabse pehle, hum check karte hain ki command dangerous to nahi hai.
Code mein `is_destructive_command` naam ka function hai. Ye check karta hai ki command mein `rm -rf /` ya `mkfs` jaise words to nahi hain.
Agar aisa koi word milta hai, to hum wahi rok dete hain aur error dete hain, taaki server ka data delete na ho jaye.

## 3. Server Details Fetch Karna

Agar command safe hai, to hum database se us `server_id` ki details nikalte hain.
Hume server ka **IP Address**, **Username**, aur **Password** chahiye hota hai connect karne ke liye.

## 4. SSH Connection (Paramiko Library)

Hum Python ki **`paramiko`** library use karte hain connection banane ke liye.
`ssh.connect()` function use karke hum remote server se judte hain, bilkul waise hi jaise aap terminal se `ssh user@ip` karte hain.

## 5. Command Execute Karna

Connection banne ke baad, `ssh.exec_command()` function wo command server par chalata hai.
Ye hume teen cheezein wapas deta hai:

1.  **stdout**: Command ka output (jo screen par dikhta hai).
2.  **stderr**: Agar koi error aaya to wo yahan milega.
3.  **exit_status**: Command successful hua (0) ya fail hua (non-zero).

## 6. Logging (Database mein save karna)

Command chalne ke baad, hum saari details record karte hain:

- Kaunsa server tha?
- Kya command chalaya?
- Kya output aaya?
- Kab chalaya (Timestamp)?

Ye sab hum MongoDB ke `command_logs` collection mein save kar dete hain taaki baad mein audit kiya ja sake.

## 7. Response Dena

Aakhri mein, hum user ko JSON format mein result bhej dete hain, jisme command ka output aur status hota hai.
