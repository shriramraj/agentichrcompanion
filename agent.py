from tools import generate_jd, build_checklist

CLARIFYING_QUESTIONS = [
    "What is your budget for each role?",
    "What are the must-have skills or experience?",
    "What is your hiring timeline?",
    "Remote or on-site preference?",
]

def parse_roles(user_input):
    """
    Extracts roles from the user_input.
    Accepts comma-separated or 'and' separated role lists.
    Examples:
        - "We need a Product Manager, a Frontend Developer and a Data Analyst"
        - "Software Engineer"
    Returns: list of dicts: [{"title": role}, ...]
    """
    import re
    # Remove prompt words
    s = user_input.lower()
    s = re.sub(r"\bwe need (an?|the)?\b", "", s)
    s = re.sub(r"\bto hire (an?|the)?\b", "", s)
    s = re.sub(r"\blooking for (an?|the)?\b", "", s)
    s = s.replace(".", "")
    # Split on ',', 'and'
    parts = re.split(r",| and ", s)
    roles = []
    for part in parts:
        role = part.strip().title()
        if role:
            roles.append({"title": role})
    return roles

def parse_answers(user_input):
    # Expects: budget; skills; timeline; location
    parts = [p.strip() for p in user_input.split(";")]
    keys = ["budget", "skills", "timeline", "location"]
    return {k: v for k, v in zip(keys, parts)}

def run_agent(user_input, state):
    output = {}

    # Step 1: If not clarified and not awaiting_clarification, treat input as hiring needs, extract roles and ask questions
    if not state.get("clarified", False) and not state.get("awaiting_clarification", False):
        roles = parse_roles(user_input)
        if not roles:
            output["error"] = "Please mention at least one role (e.g. 'Product Manager', 'Frontend Developer')."
            return output, {"roles": [], "clarified": False, "answers": {}, "awaiting_clarification": False}
        output["clarifying_questions"] = CLARIFYING_QUESTIONS
        output["message"] = "Please answer the following clarifying questions for better accuracy."
        return output, {"roles": roles, "clarified": False, "answers": {}, "awaiting_clarification": True}

    # Step 2: If awaiting clarification, treat input as clarifying answers
    if state.get("awaiting_clarification", False) and not state.get("clarified", False):
        answers = parse_answers(user_input)
        if len(answers) < 4:
            output["error"] = "Please answer all questions, separated by semicolons (;)."
            output["clarifying_questions"] = CLARIFYING_QUESTIONS
            return output, {
                "roles": state.get("roles", []),
                "clarified": False,
                "answers": {},
                "awaiting_clarification": True,
            }
        roles = state.get("roles", [])
        job_descriptions = [generate_jd(role, answers) for role in roles]
        checklists = [build_checklist(role, answers) for role in roles]
        output = {
            "roles": roles,
            "job_descriptions": job_descriptions,
            "checklists": checklists,
        }
        return output, {
            "roles": roles,
            "clarified": True,
            "answers": answers,
            "awaiting_clarification": False,
        }

    # Step 3: If clarified, just show results again
    if state.get("clarified", False):
        roles = state.get("roles", [])
        answers = state.get("answers", {})
        job_descriptions = [generate_jd(role, answers) for role in roles]
        checklists = [build_checklist(role, answers) for role in roles]
        output = {
            "roles": roles,
            "job_descriptions": job_descriptions,
            "checklists": checklists,
        }
        return output, state

    output["error"] = "Unknown state. Please refresh and start again."
    return output, {"roles": [], "clarified": False, "answers": {}, "awaiting_clarification": False}