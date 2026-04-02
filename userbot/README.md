# Telegram UserBot

Bu bot, siz məşğul olduğunuz vaxt gələn şəxsi mesajlara (PM) avtomatik cavab verir və israrla mesaj yazanları bloklayır.

## 📱 Termux Üzərində Quraşdırma

Telegram botunu Android telefonunuzda (Termux) 7/24 işlək vəziyyətə gətirmək üçün aşağıdakı addımları izləyin:

### 1️⃣ Termux-u Yeniləyin və Lazımi Paketləri Yükləyin
İlk öncə Termux-u açıb aşağıdakı əmrləri daxil edin:
```bash
pkg update && pkg upgrade -y
pkg install python git -y
```

### 2️⃣ Repozitoriyanı Klonlayın
Layihəni GitHub-dan Termux-a yükləmək üçün aşağıdakı klonlama əmrini işlədin:
```bash
git clone https://github.com/Ysvvv/UserBot.git
```

### 3️⃣ Qovluğa Daxil Olun və Asılılıqları Quraşdırın
Faylların olduğu qovluğa girmək və lazımi kitabxanaları (`telethon`) yükləmək üçün:
```bash
cd UserBot/userbot
pip install -r requirements.txt
```

### 4️⃣ Botu İşə Salın və Hesabınızı Qoşun
Hazırlıqlar tamamlandı! İndi botu işə salmaq üçün bu əmri yazın:
```bash
python userbot.py
```

**İlk Dəfə İşə Salarkən:**
1. Bot ilk olaraq sizdən `API_ID` və `API_HASH` məlumatlarını istəyəcək.
   > Bu məlumatları [my.telegram.org](https://my.telegram.org) saytına daxil olaraq "API development tools" bölməsindən əldə edə bilərsiniz.
2. Bu məlumatları daxil etdikdən sonra sistem onları təhlükəsiz şəkildə cihazınızda (`config.json`-da) yadda saxlayacaq. (Özünüz bu faylı silənə qədər bir daha istənməyəcək.)
3. Daha sonra bot telefon nömrənizi (`+994...` formatında) daxil etməyinizi xahiş edəcək. Nömrəni daxil edib, Telegram tətbiqinizə gələn təsdiq kodunu terminala yazın.

Bununla da bot artıq arxa planda mesajlarınıza nəzarət edir.

## ⚡ Qeydlər
- **Təhlükəsizlik:** Sizin `API_ID`, `API_HASH`, və sessiya fayllarınız (`.session`) gizli fayllardır və avtomatik `gitignore` tərəfindən idarə edilir, yəni ehtiyatla bu kodlarınızı silsəniz və ya paylaşsanız bu dəyərlər GitHub-a yüklənməyəcək.
- **Botu Bağlamaq:** Botu dayandırmaq istəsəniz, sadəcə Termux-da eyni anda `CTRL + C` düymələrinə basa bilərsiniz.
