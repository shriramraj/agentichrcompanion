def generate_jd(role, answers):
    title = role.get("title", "Unknown Role")
    budget = answers.get("budget", "N/A")
    timeline = answers.get("timeline", "N/A")
    skills = answers.get("skills", "N/A")
    location = answers.get("location", "N/A")
    return f"""
✨ **{title} – Role Spellbook** ✨

**💰 Budget:** {budget}  
**⏳ Timeline:** {timeline}  
**🛠️ Must-have skills:** {skills}  
**🌍 Location:** {location}

**🔮 Your Quest:**  
- Shape the future of our adventure as a {title}  
- Channel your magic to craft, build, and inspire  
- Collaborate with a guild of visionaries

**🪄 What You Bring:**  
- Proven mastery in your craft  
- Passion for innovation and impact  
- The right skills to turn dreams into reality
"""

def build_checklist(role, answers):
    title = role.get("title", "Unknown Role")
    return [
        f"🔎 Confirm the magical budget for **{title}**: {answers.get('budget', 'N/A')}",
        f"📜 List the must-have spells/skills for **{title}**: {answers.get('skills', 'N/A')}",
        f"🗓️ Set the quest timeline for **{title}**: {answers.get('timeline', 'N/A')}",
        f"🌐 Decide if this quest is remote or on-site: {answers.get('location', 'N/A')}",
        f"📝 Draft and post the enchanted job description for **{title}**",
        f"🧙 Review applicants and shortlist magical talent for **{title}**",
        f"🤝 Schedule interviews with the guild for **{title}**",
        f"🎉 Welcome your new {title} to the fellowship!",
    ]