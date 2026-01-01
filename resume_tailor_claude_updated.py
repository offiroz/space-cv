import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from anthropic import Anthropic
from dotenv import load_dotenv

# טעינת משתני סביבה מקובץ .env
load_dotenv()

# אתחול Flask
app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)  # מאפשר גישה מדפדפן

# אתחול Claude client
api_key = os.getenv("ANTHROPIC_API_KEY", "YOUR_API_KEY_HERE")
client = Anthropic(api_key=api_key)

# הגדרת מודל
MODEL = "claude-sonnet-4-20250514"


def tailor_resume(original_resume, job_description):
    """
    התאמת קורות חיים לתיאור משרה ספציפי
    """
    
    prompt = f"""אתה מומחה בכתיבה והתאמה של קורות חיים למשרות ספציפיות.
התפקיד שלך הוא לעזור למועמדים להציג את עצמם בצורה הטובה ביותר עבור משרה מסוימת.

חשוב: אל תמציא מידע שלא קיים בקורות החיים המקוריים. התאם רק את האופן שבה המידע הקיים מוצג.

---

אני מצרף כאן שני טקסטים: את קורות החיים שלי ואת תיאור המשרה שאליה אני רוצה להתמיין.

המטרה שלך היא לעזור לי להתאים את קורות החיים למשרה בצורה אופטימלית, תוך שמירה על הכללים הבאים:

1. **אמינות מעל הכל**: אל תמציא ניסיון, תארים או כישורים שאינם מופיעים בקורות החיים המקוריים שלי.

2. **שימוש במילות מפתח**: זהה את מילות המפתח וכישורי הליבה בתיאור המשרה ושזור אותם בתוך קורות החיים שלי (במקומות שבהם הם רלוונטיים למה שבאמת עשיתי).

3. **שינוי סדרי עדיפויות**: אם בתיאור המשרה דורשים יכולת מסוימת שיש לי אך היא מופיעה בסוף הרשימה אצלי, הקדם אותה להתחלה.

4. **ניסוח הישגים**: נסח מחדש את תיאורי התפקיד שלי כך שיהיו ממוקדי תוצאות (Impact) ורלוונטיים לדרישות המשרה החדשה.

5. **סיכום מקצועי**: כתוב 'תקציר' (Summary) קצר של 3-4 שורות לראש קורות החיים שמדגיש בדיוק למה אני המועמד המתאים למשרה הספציפית הזו.

6. **אורך מותאם**: אם הקורות חיים ארוכים מדי ויש חפיפה של שנים או משרות לא רלוונטיות למשרה הנוכחית, תוכל לוותר על משרה אחת או יותר כדי לשמור על תמציתיות (1-2 עמודים מקסימום).

---

**קורות החיים המקוריים שלי:**

{original_resume}

---

**תיאור המשרה:**

{job_description}

---

אנא החזר את קורות החיים המותאמים בפורמט ברור ומסודר.

הוראות נוספות:
- אם שואלים אותך שאלה אחרת שאינה קשורה לנושא התאמת קורות חיים, החזר: "סליחה אבל אני יכול לענות רק בנושאים שקשורים לקורות החיים"
- התמקד בניסוח הישגים בפורמט: "פעולה + תוצאה מדידה" (כאשר זה אפשרי)"""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4000,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
    
    except Exception as e:
        raise Exception(f"שגיאה בקריאה ל-API: {str(e)}")


def analyze_match(original_resume, job_description, tailored_resume):
    """
    ניתוח התאמה בין קורות חיים לתיאור משרה
    """
    
    analysis_prompt = f"""נתח את ההתאמה בין קורות החיים המותאמים לתיאור המשרה.

תיאור המשרה:
{job_description}

קורות חיים מותאמים:
{tailored_resume}

ספק:
1. אחוז התאמה משוער (0-100%)
2. כישורים שמופיעים במשרה ונמצאו בקורות החיים
3. כישורים שמופיעים במשרה אך חסרים בקורות החיים
4. המלצות לשיפור נוסף"""

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            temperature=0.2,
            messages=[
                {
                    "role": "user", 
                    "content": f"אתה מומחה HR ומנתח התאמות בין מועמדים למשרות.\n\n{analysis_prompt}"
                }
            ]
        )
        
        return response.content[0].text
    
    except Exception as e:
        raise Exception(f"שגיאה בניתוח: {str(e)}")


# נקודות קצה (API Endpoints)

@app.route('/')
def index():
    """משרת את הדף הראשי"""
    return send_from_directory('frontend', 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """בדיקת תקינות השרת"""
    return jsonify({
        "status": "ok",
        "message": "השרת פעיל ורץ",
        "api_configured": api_key != "YOUR_API_KEY_HERE"
    })


@app.route('/api/tailor', methods=['POST'])
def api_tailor():
    """
    API להתאמת קורות חיים
    
    Expected JSON:
    {
        "resume": "קורות החיים המקוריים",
        "job_description": "תיאור המשרה"
    }
    """
    try:
        # קבלת הנתונים מה-request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "לא התקבלו נתונים"
            }), 400
        
        resume = data.get('resume', '').strip()
        job_description = data.get('job_description', '').strip()
        
        # בדיקת תקינות
        if not resume:
            return jsonify({
                "success": False,
                "error": "חסרים קורות חיים"
            }), 400
            
        if not job_description:
            return jsonify({
                "success": False,
                "error": "חסר תיאור משרה"
            }), 400
        
        # בדיקת API key
        if api_key == "YOUR_API_KEY_HERE":
            return jsonify({
                "success": False,
                "error": "לא הוגדר API key. אנא הוסף את ה-ANTHROPIC_API_KEY בקובץ .env"
            }), 500
        
        # הרצת ההתאמה
        tailored_resume = tailor_resume(resume, job_description)
        
        return jsonify({
            "success": True,
            "tailored_resume": tailored_resume
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """
    API לניתוח התאמה
    
    Expected JSON:
    {
        "resume": "קורות החיים המקוריים",
        "job_description": "תיאור המשרה",
        "tailored_resume": "קורות החיים המותאמים"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "לא התקבלו נתונים"
            }), 400
        
        resume = data.get('resume', '').strip()
        job_description = data.get('job_description', '').strip()
        tailored_resume = data.get('tailored_resume', '').strip()
        
        if not all([resume, job_description, tailored_resume]):
            return jsonify({
                "success": False,
                "error": "חסרים נתונים לניתוח"
            }), 400
        
        # הרצת הניתוח
        analysis = analyze_match(resume, job_description, tailored_resume)
        
        return jsonify({
            "success": True,
            "analysis": analysis
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# הרצת השרת
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)