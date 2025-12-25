
import json
import os

def generate_dataset():
    """
    Generates a 'Gold Standard' pilot dataset of 20 Resume-JD pairs 
    with Ground Truth labels (High, Medium, Low).
    This dataset is used to benchmark the accuracy of SBERT vs TF-IDF.
    """
    
    dataset = [
        # --- HIGH MATCH (Ground Truth: 1.0) ---
        # Perfect semantic and keyword alignment
        {
            "id": 1,
            "resume_text": "Senior Python Developer with 5 years of experience in Django, Flask, and AWS. Expert in REST APIs, PostgreSQL, and Docker.",
            "jd_text": "Looking for a Senior Python Developer. Must have experience with Django, Flask, AWS, and building RESTful APIs. PostgreSQL and Docker knowledge required.",
            "ground_truth_label": "High",
            "ground_truth_score": 1.0
        },
        {
            "id": 2,
            "resume_text": "Data Scientist proficient in Python, Pandas, Scikit-Learn, and TensorFlow. Experience with machine learning models and data visualization using Matplotlib.",
            "jd_text": "Data Scientist role. Requirements: Python, Pandas, Scikit-Learn, TensorFlow. Strong background in ML models and visualization tools like Matplotlib.",
            "ground_truth_label": "High",
            "ground_truth_score": 1.0
        },
        {
            "id": 3,
            "resume_text": "Frontend Engineer skilled in React.js, Redux, HTML5, CSS3, and JavaScript. Experienced in building responsive UIs and integrating REST APIs.",
            "jd_text": "We need a Frontend Engineer with React.js, Redux, HTML, CSS, and JS skills. Responsibilities include creating responsive UIs and API integration.",
            "ground_truth_label": "High",
            "ground_truth_score": 1.0
        },
        {
            "id": 4,
            "resume_text": "DevOps Engineer with expertise in Kubernetes, Jenkins, Terraform, and Azure. Strong background in CI/CD pipelines and cloud infrastructure.",
            "jd_text": "Hiring DevOps Engineer. Skills: Kubernetes, Jenkins, Terraform, Azure. Must manage CI/CD pipelines and cloud infra.",
            "ground_truth_label": "High",
            "ground_truth_score": 1.0
        },
        {
            "id": 5,
            "resume_text": "Full Stack Developer. Tech stack: Node.js, Express, MongoDB, and Angular. Experience in building scalable web applications.",
            "jd_text": "Full Stack Developer needed. Proficient in Node.js, Express, MongoDB, Angular. Build scalable web apps.",
            "ground_truth_label": "High",
            "ground_truth_score": 1.0
        },

        # --- MEDIUM MATCH (Ground Truth: ~0.5 - 0.7) ---
        # Semantic overlap but vocabulary mismatch (SBERT should win here)
        {
            "id": 6,
            "resume_text": "Backend Engineer. Skilled in building server-side logic using Go and microservices architecture. Familiar with containerization and orchestration.",
            "jd_text": "We are looking for a Golang Developer to work on distributed systems. Knowledge of Docker and Kubernetes is a plus.",
            "ground_truth_label": "Medium",
            "ground_truth_score": 0.7
        },
        {
            "id": 7,
            "resume_text": "AI Researcher focused on Deep Learning and Natural Language Processing. Published papers on Transformer models and large language models.",
            "jd_text": "Machine Learning Engineer role. Experience with NLP, BERT, GPT, and neural networks is highly desirable.",
            "ground_truth_label": "Medium",
            "ground_truth_score": 0.7
        },
        {
            "id": 8,
            "resume_text": "Web Designer with a portfolio of user-centric designs. Proficient in Adobe XD, Figma, and prototyping tools. Strong understanding of UX principles.",
            "jd_text": "UI/UX Designer. Requirements: Wireframing, visual design, user research. Experience with Sketch or InVision preferred.",
            "ground_truth_label": "Medium",
            "ground_truth_score": 0.6
        },
        {
            "id": 9,
            "resume_text": "System Administrator. Managed Linux servers, shell scripting, and network security. Certified in Red Hat System Administration.",
            "jd_text": "Infrastructure Engineer. Responsibilities: Server maintenance, bash scripting, firewall configuration. RHCSA certification is a bonus.",
            "ground_truth_label": "Medium",
            "ground_truth_score": 0.7
        },
        {
            "id": 10,
            "resume_text": "Mobile App Developer. Built several iOS applications using Swift and Objective-C. Familiar with Apple's Human Interface Guidelines.",
            "jd_text": "iOS Developer needed. Experience with native iOS development tools. Knowledge of mobile UI/UX best practices.",
            "ground_truth_label": "Medium",
            "ground_truth_score": 0.7
        },
        
         # --- LOW MATCH (Ground Truth: 0.0 - 0.2) ---
         # Completely irrelevant domains
        {
            "id": 11,
            "resume_text": "Executive Chef with 10 years of culinary experience. Expert in French and Italian cuisine. Managed kitchen staff of 20.",
            "jd_text": "Senior Java Developer. Requirements: Spring Boot, Hibernate, SQL. Must lead a team of software engineers.",
            "ground_truth_label": "Low",
            "ground_truth_score": 0.1
        },
        {
            "id": 12,
            "resume_text": "Sales Manager. A proven track record of exceeding revenue targets. Skilled in CRM software, negotiation, and lead generation.",
            "jd_text": "Database Administrator. Manage Oracle and SQL Server databases. Perform backups, tuning, and security patches.",
            "ground_truth_label": "Low",
            "ground_truth_score": 0.1
        },
        {
            "id": 13,
            "resume_text": "Graphic Designer. Logos, brochures, and brand identity. Expert in Photoshop and Illustrator.",
            "jd_text": "Network Engineer. Cisco CCNA required. Experience with routers, switches, and VPN configuration.",
            "ground_truth_label": "Low",
            "ground_truth_score": 0.1
        },
        {
            "id": 14,
            "resume_text": "Registered Nurse. ICU experience. Compassionate patient care and medication administration.",
            "jd_text": "Cloud Architect. AWS professional certification required. Design high-availability cloud solutions.",
            "ground_truth_label": "Low",
            "ground_truth_score": 0.0
        },
         {
            "id": 15,
            "resume_text": "High School English Teacher. Literature analysis, curriculum development, and classroom management.",
            "jd_text": "Embedded Systems Engineer. C/C++ programming for microcontrollers. Experience with RTOS.",
            "ground_truth_label": "Low",
            "ground_truth_score": 0.0
        },
        
        # --- MIXED/TRICKY CASE (Ground Truth: 0.4 - 0.5) ---
        # Keyword match but partial irrelevance or junior vs senior mismatch
        {
            "id": 16,
            "resume_text": "Junior Python Developer. Fresh graduate. Learned Python syntax and basic scripting.",
            "jd_text": "Principal Software Architect. 15+ years experience. Expert in distributed systems and high-level strategy.",
            "ground_truth_label": "Low-Medium",
            "ground_truth_score": 0.3
        },
        {
            "id": 17,
            "resume_text": "Customer Support Representative. Handling tickets, answering calls, and troubleshooting basic issues.",
            "jd_text": "Technical Support Engineer. Debugging code, SQL queries, and log analysis.",
            "ground_truth_label": "Medium",
            "ground_truth_score": 0.5
        },
        {
            "id": 18,
            "resume_text": "Marketing Intern. Social media management and content creation.",
            "jd_text": "Chief Marketing Officer. Strategic vision, budget management, and global brand direction.",
            "ground_truth_label": "Low-Medium",
            "ground_truth_score": 0.2
        },
        {
            "id": 19,
            "resume_text": "Accountant. CPA certified. Financial reporting, tax preparation, and auditing.",
            "jd_text": "Financial Analyst. Financial modeling, forecasting, and data analysis expert.",
            "ground_truth_label": "Medium-High",
            "ground_truth_score": 0.6
        },
        {
            "id": 20,
            "resume_text": "Project Manager. Agile certification (CSM). Managed software delivery teams and sprint planning.",
            "jd_text": "Product Owner. Define product roadmap, backlog grooming, and stakeholder management.",
            "ground_truth_label": "High",
            "ground_truth_score": 0.8
        }
    ]
    
    output_path = "dataset.json"
    with open(output_path, "w") as f:
        json.dump(dataset, f, indent=4)
        
    print(f"Generated {len(dataset)} pairs in 'dataset.json'.")

if __name__ == "__main__":
    generate_dataset()
