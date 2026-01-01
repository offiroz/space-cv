# Space CV - משגרים את הקריירה שלך לחלל 🚀

מערכת אוטומטית להתאמת קורות חיים למשרות ספציפיות באמצעות AI.

## תכונות

✨ **התאמה אוטומטית** - המערכת מתאימה את קורות החיים שלך לכל משרה  
📊 **ניתוח התאמה** - קבל אחוז התאמה והמלצות לשיפור  
🎨 **עיצוב חלל** - ממשק משתמש מעוצב בנושא חלל ואסטרונאוטים  
🔒 **מאובטח** - API key מאוחסן בצורה מאובטחת

## טכנולוגיות

- **Backend**: Flask (Python)
- **AI**: Claude 4 (Anthropic)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Railway

## התקנה מקומית

1. שכפל את הפרויקט:
```bash
git clone https://github.com/USERNAME/space-cv.git
cd space-cv
```

2. התקן dependencies:
```bash
pip install -r requirements.txt
```

3. צור קובץ `.env` והוסף את ה-API key שלך:
```
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
```

4. הרץ את השרת:
```bash
python app.py
```

5. פתח דפדפן בכתובת: `http://localhost:5000`

## שימוש

1. הדבק את קורות החיים שלך בתיבה הימנית
2. הדבק את תיאור המשרה בתיבה השמאלית
3. לחץ על "התאם קורות חיים" או "נתח התאמה"
4. קבל תוצאות מותאמות אישית

## פרסום ב-Railway

1. צור חשבון ב-[Railway.app](https://railway.app)
2. התחבר עם GitHub
3. לחץ "New Project" → "Deploy from GitHub repo"
4. בחר את הפרויקט
5. הוסף את ה-API key במשתני סביבה (Environment Variables):
   - Key: `ANTHROPIC_API_KEY`
   - Value: `sk-ant-api03-YOUR_KEY_HERE`

## רישיון

MIT License - עופר

## צור קשר

לשאלות ובעיות, פתח Issue בגיטהאב.
