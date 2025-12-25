
import json
import random
from typing import List, Dict

class ResumeJDGenerator:
    def __init__(self):
        self.roles = [
            "Machine Learning Engineer",
            "Full Stack Developer", 
            "DevOps Engineer",
            "Data Scientist",
            "Frontend Developer",
            "Backend Developer",
            "Mobile Developer",
            "Security Engineer",
            "QA Engineer",
            "Cloud Architect"
        ]
        
        self.experience_levels = ["Junior", "Mid-Level", "Senior"]

        self.skills_db = {
            "Machine Learning Engineer": ["Python", "TensorFlow", "PyTorch", "Scikit-Learn", "NLP", "Computer Vision", "AWS SageMaker"],
            "Full Stack Developer": ["JavaScript", "React", "Node.js", "MongoDB", "Express", "HTML/CSS", "TypeScript"],
            "DevOps Engineer": ["Docker", "Kubernetes", "Jenkins", "Terraform", "AWS", "CI/CD", "Linux"],
            "Data Scientist": ["Python", "Pandas", "NumPy", "SQL", "Tableau", "Statistics", "Machine Learning"],
            "Frontend Developer": ["React", "Vue.js", "Angular", "HTML5", "CSS3", "JavaScript", "Responsive Design"],
            "Backend Developer": ["Java", "Spring Boot", "Python", "Django", "Go", "PostgreSQL", "Redis"],
            "Mobile Developer": ["Swift", "iOS", "Kotlin", "Android", "React Native", "Flutter", "Mobile UI"],
            "Security Engineer": ["Network Security", "Penetration Testing", "Cryptography", "Firewall", "SIEM", "OWASP", "Python"],
            "QA Engineer": ["Selenium", "Appium", "JIRA", "Test Automation", "Python", "Java", "Bug Tracking"],
            "Cloud Architect": ["AWS", "Azure", "Google Cloud", "Microservices", "System Design", "Scalability", "Security"]
        }

        self.match_descriptions = {
             "High": "Perfect match. Candidate has all required skills and experience level matches.",
             "Medium-High": "Strong match. Candidate has most skills but maybe slightly less experience or missing one niche tool.",
             "Medium": "Good match. Candidate has core skills but missing several secondary skills or different industry background.",
             "Low-Medium": "Weak match. Candidate is from related field but lacks specific tech stack (e.g. Java dev applied for Python role).",
             "Low": "No match. Completely different role (e.g. Chef applied for Developer)."
        }

    def generate_jd(self, role: str, level: str) -> str:
        """Generate job description"""
        skills = ", ".join(self.skills_db.get(role, []))
        return f"Hiring {level} {role}. Required skills: {skills}. We are looking for a professional with strong background in these technologies to join our team."
    
    def generate_resume(self, role: str, level: str, match_level: str) -> str:
        """Generate resume with controlled match quality"""
        base_skills = self.skills_db.get(role, [])
        
        if match_level == "High":
             # Use all skills, correct role
             skills_text = ", ".join(base_skills)
             return f"{level} {role} with expertise in {skills_text}. Proven track record of delivering projects using these technologies."
        
        elif match_level == "Medium-High":
             # Use 80% of skills
             subset = base_skills[:max(1, int(len(base_skills)*0.8))]
             skills_text = ", ".join(subset)
             return f"{level} {role} experienced in {skills_text}. Fast learner and team player."
             
        elif match_level == "Medium":
             # Use 50% of skills
             subset = base_skills[:max(1, int(len(base_skills)*0.5))]
             skills_text = ", ".join(subset)
             return f"Professional with exprience in {skills_text}. Looking to transition into {role} role."

        elif match_level == "Low-Medium":
             # Related field but different stack (e.g. slight mismatch)
             # For simplicity, let's just pick a random OTHER role's skills
             other_role = random.choice([r for r in self.roles if r != role])
             other_skills = self.skills_db.get(other_role, [])
             skills_text = ", ".join(other_skills[:3])
             return f"{level} {other_role} with skills in {skills_text}. Interested in learning {role} technologies."
             
        elif match_level == "Low":
             # Completely different
             irrelevant_jobs = ["Chef", "Driver", "Nurse", "Teacher", "Sales Associate"]
             job = random.choice(irrelevant_jobs)
             return f"Experienced {job}. Skills include time management, communication, and organization. Hard worker."
             
        return ""

    def get_score_for_label(self, label: str) -> float:
        mapping = {
            "High": 1.0,
            "Medium-High": 0.8,
            "Medium": 0.6,
            "Low-Medium": 0.4,
            "Low": 0.0
        }
        return mapping.get(label, 0.0)
    
    def generate_100_pairs(self) -> List[Dict]:
        pairs = []
        pair_id = 1
        
        # We need 100 pairs. 
        # 10 Roles * 2 variations per level/match combo?
        # User suggested: 5 match levels * 20 pairs each = 100 total
        # Distribution: 20 per match level.
        
        # Let's iterate through roles and ensure we get even distribution
        # 10 roles. For each role, we generate 10 pairs (2 of each match level).
        # Total = 10 * 10 = 100.
        
        match_levels = ["High", "Medium-High", "Medium", "Low-Medium", "Low"]
        
        for role in self.roles:  # 10 roles
            # For each role, pick a random level for the JD
            level = random.choice(self.experience_levels)
            jd_text = self.generate_jd(role, level)
            
            for m_level in match_levels:
                # Generate 2 variations for this match level
                for _ in range(2):
                    resume_text = self.generate_resume(role, level, m_level)
                    
                    pairs.append({
                        "id": pair_id,
                        "resume_text": resume_text,
                        "jd_text": jd_text,
                        "ground_truth_label": m_level,
                        "ground_truth_score": self.get_score_for_label(m_level),
                        "role": role,
                        "level": level
                    })
                    pair_id += 1
                
        return pairs

if __name__ == "__main__":
    gen = ResumeJDGenerator()
    pairs = gen.generate_100_pairs()
    
    # Overwrite the main dataset.json so benchmarks pick it up
    with open("dataset.json", "w") as f:
        json.dump(pairs, f, indent=4)
    
    print(f"Generated {len(pairs)} pairs in 'dataset.json'")
