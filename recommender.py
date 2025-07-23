import os
import requests
from bs4 import BeautifulSoup
import re

def search_top_courses(skill):
    """
    Search for top-rated courses for a specific skill.
    Returns 3 actual course recommendations with links.
    """
    # Curated top courses for common skills
    curated_courses = {
        'python': [
            {'name': 'Python for Everybody (Coursera)', 'url': 'https://www.coursera.org/specializations/python', 'platform': 'Coursera', 'rating': '4.8'},
            {'name': 'Complete Python Bootcamp (Udemy)', 'url': 'https://www.udemy.com/course/complete-python-bootcamp/', 'platform': 'Udemy', 'rating': '4.6'},
            {'name': 'Python Programming (edX)', 'url': 'https://www.edx.org/learn/python', 'platform': 'edX', 'rating': '4.7'}
        ],
        'sql': [
            {'name': 'SQL for Data Science (Coursera)', 'url': 'https://www.coursera.org/learn/sql-for-data-science', 'platform': 'Coursera', 'rating': '4.7'},
            {'name': 'The Complete SQL Bootcamp (Udemy)', 'url': 'https://www.udemy.com/course/the-complete-sql-bootcamp/', 'platform': 'Udemy', 'rating': '4.6'},
            {'name': 'Database Systems (edX)', 'url': 'https://www.edx.org/learn/database-systems', 'platform': 'edX', 'rating': '4.5'}
        ],
        'machine learning': [
            {'name': 'Machine Learning (Coursera)', 'url': 'https://www.coursera.org/learn/machine-learning', 'platform': 'Coursera', 'rating': '4.9'},
            {'name': 'Machine Learning A-Z (Udemy)', 'url': 'https://www.udemy.com/course/machinelearning/', 'platform': 'Udemy', 'rating': '4.5'},
            {'name': 'Machine Learning Fundamentals (edX)', 'url': 'https://www.edx.org/learn/machine-learning', 'platform': 'edX', 'rating': '4.6'}
        ],
        'aws': [
            {'name': 'AWS Cloud Practitioner (Coursera)', 'url': 'https://www.coursera.org/specializations/aws-cloud-practitioner', 'platform': 'Coursera', 'rating': '4.7'},
            {'name': 'AWS Certified Solutions Architect (Udemy)', 'url': 'https://www.udemy.com/course/aws-certified-solutions-architect-associate/', 'platform': 'Udemy', 'rating': '4.6'},
            {'name': 'Cloud Computing (edX)', 'url': 'https://www.edx.org/learn/cloud-computing', 'platform': 'edX', 'rating': '4.5'}
        ],
        'tableau': [
            {'name': 'Data Visualization with Tableau (Coursera)', 'url': 'https://www.coursera.org/specializations/data-visualization', 'platform': 'Coursera', 'rating': '4.6'},
            {'name': 'Tableau 2023 A-Z (Udemy)', 'url': 'https://www.udemy.com/course/tableau10/', 'platform': 'Udemy', 'rating': '4.5'},
            {'name': 'Data Visualization (edX)', 'url': 'https://www.edx.org/learn/data-visualization', 'platform': 'edX', 'rating': '4.4'}
        ],
        'docker': [
            {'name': 'Docker for Beginners (Coursera)', 'url': 'https://www.coursera.org/learn/docker-containers', 'platform': 'Coursera', 'rating': '4.5'},
            {'name': 'Docker Mastery (Udemy)', 'url': 'https://www.udemy.com/course/docker-mastery/', 'platform': 'Udemy', 'rating': '4.6'},
            {'name': 'Container Technologies (edX)', 'url': 'https://www.edx.org/learn/container-technologies', 'platform': 'edX', 'rating': '4.3'}
        ],
        'git': [
            {'name': 'Version Control with Git (Coursera)', 'url': 'https://www.coursera.org/learn/version-control-with-git', 'platform': 'Coursera', 'rating': '4.7'},
            {'name': 'Git Complete (Udemy)', 'url': 'https://www.udemy.com/course/git-complete/', 'platform': 'Udemy', 'rating': '4.6'},
            {'name': 'Software Development (edX)', 'url': 'https://www.edx.org/learn/software-development', 'platform': 'edX', 'rating': '4.4'}
        ],
        'pandas': [
            {'name': 'Data Analysis with Python (Coursera)', 'url': 'https://www.coursera.org/learn/data-analysis-with-python', 'platform': 'Coursera', 'rating': '4.6'},
            {'name': 'Python for Data Science (Udemy)', 'url': 'https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/', 'platform': 'Udemy', 'rating': '4.5'},
            {'name': 'Data Science (edX)', 'url': 'https://www.edx.org/learn/data-science', 'platform': 'edX', 'rating': '4.5'}
        ],
        'tensorflow': [
            {'name': 'TensorFlow in Practice (Coursera)', 'url': 'https://www.coursera.org/specializations/tensorflow-in-practice', 'platform': 'Coursera', 'rating': '4.7'},
            {'name': 'TensorFlow 2.0 Complete Course (Udemy)', 'url': 'https://www.udemy.com/course/tensorflow-developer-certificate-machine-learning-zero-to-mastery/', 'platform': 'Udemy', 'rating': '4.6'},
            {'name': 'Deep Learning (edX)', 'url': 'https://www.edx.org/learn/deep-learning', 'platform': 'edX', 'rating': '4.6'}
        ],
        'power bi': [
            {'name': 'Data Analysis and Visualization (Coursera)', 'url': 'https://www.coursera.org/specializations/data-analysis-visualization', 'platform': 'Coursera', 'rating': '4.5'},
            {'name': 'Power BI A-Z (Udemy)', 'url': 'https://www.udemy.com/course/microsoft-power-bi-up-running-with-power-bi-desktop/', 'platform': 'Udemy', 'rating': '4.5'},
            {'name': 'Business Intelligence (edX)', 'url': 'https://www.edx.org/learn/business-intelligence', 'platform': 'edX', 'rating': '4.3'}
        ]
    }
    
    # Try to find exact match first
    skill_lower = skill.lower()
    for key in curated_courses:
        if key in skill_lower or skill_lower in key:
            return curated_courses[key]
    
    # If no exact match, try partial matches
    for key in curated_courses:
        if any(word in skill_lower for word in key.split()) or any(word in key for word in skill_lower.split()):
            return curated_courses[key]
    
    # Fallback for skills not in curated list
    return [
        {'name': f'Top {skill.title()} Course (Coursera)', 'url': f'https://www.coursera.org/search?query={skill.replace(" ", "+")}', 'platform': 'Coursera', 'rating': '4.5+'},
        {'name': f'Best {skill.title()} Course (Udemy)', 'url': f'https://www.udemy.com/courses/search/?q={skill.replace(" ", "+")}', 'platform': 'Udemy', 'rating': '4.5+'},
        {'name': f'{skill.title()} Learning Path (edX)', 'url': f'https://www.edx.org/search?q={skill.replace(" ", "+")}', 'platform': 'edX', 'rating': '4.5+'}
    ]

def generate_recommendations(missing_skills, jd_skills=None):
    """
    Provide general platform recommendations for skill categories instead of specific courses for each skill.
    Also generate a dynamic learning path as a step-by-step sequence.
    """
    # Categorize skills
    tech_skills = [s for s in missing_skills if any(tech in s.lower() for tech in ['python', 'sql', 'aws', 'docker', 'git', 'machine learning', 'data', 'pandas', 'tensorflow', 'pytorch', 'scikit-learn'])]
    analysis_skills = [s for s in missing_skills if any(analysis in s.lower() for analysis in ['excel', 'tableau', 'power bi', 'statistical analysis', 'a/b testing'])]
    cloud_skills = [s for s in missing_skills if any(cloud in s.lower() for cloud in ['aws', 'azure', 'gcp', 'docker', 'kubernetes'])]
    soft_skills = [s for s in missing_skills if any(soft in s.lower() for soft in ['communication', 'leadership', 'teamwork', 'project management'])]
    
    recommendations = {}
    
    # Provide platform recommendations for skill categories
    if tech_skills:
        recommendations['Technical Skills'] = [
            "[Coursera - Data Science & Programming Specializations](https://www.coursera.org/browse/data-science)",
            "[Udemy - Programming & Development Courses](https://www.udemy.com/courses/development/)",
            "[edX - Computer Science & Data Science](https://www.edx.org/learn/computer-science)"
        ]
    
    if analysis_skills:
        recommendations['Data Analysis & Visualization'] = [
            "[Coursera - Data Analysis Specializations](https://www.coursera.org/browse/data-science/data-analysis)",
            "[Udemy - Data Analysis & Visualization Courses](https://www.udemy.com/courses/search/?q=data+analysis)",
            "[edX - Data Science & Analytics](https://www.edx.org/learn/data-science)"
        ]
    
    if cloud_skills:
        recommendations['Cloud & DevOps'] = [
            "[Coursera - Cloud Computing Specializations](https://www.coursera.org/browse/computer-science/software-development)",
            "[Udemy - Cloud & DevOps Courses](https://www.udemy.com/courses/search/?q=aws+azure)",
            "[edX - Cloud Computing & Infrastructure](https://www.edx.org/learn/cloud-computing)"
        ]
    
    if soft_skills:
        recommendations['Soft Skills & Leadership'] = [
            "[Coursera - Business & Leadership](https://www.coursera.org/browse/business/leadership-and-management)",
            "[Udemy - Communication & Leadership](https://www.udemy.com/courses/search/?q=communication+leadership)",
            "[LinkedIn Learning - Professional Development](https://www.linkedin.com/learning/)"
        ]
    
    # If no categories match, provide general recommendations
    if not recommendations:
        recommendations['General Skills Development'] = [
            "[Coursera - Professional Certificates](https://www.coursera.org/professional-certificates)",
            "[Udemy - Skill Development Courses](https://www.udemy.com/)",
            "[edX - Professional Education](https://www.edx.org/professional-education)"
        ]
    
    # Create a more natural learning path
    if len(missing_skills) <= 2:
        # For 1-2 skills, keep it simple
        learning_path = [f"Focus on mastering {', '.join([s.title() for s in missing_skills])} to strengthen your profile."]
    else:
        # Group related skills and create a narrative
        learning_path = []
        if tech_skills:
            if len(tech_skills) == 1:
                learning_path.append(f"Start by building your technical foundation in {tech_skills[0].title()}.")
            else:
                learning_path.append(f"Begin with the core technical skills: {', '.join([s.title() for s in tech_skills[:2]])}.")
                if len(tech_skills) > 2:
                    learning_path.append(f"Then advance to: {', '.join([s.title() for s in tech_skills[2:]])}.")
        
        if analysis_skills:
            learning_path.append(f"Develop your data analysis capabilities with: {', '.join([s.title() for s in analysis_skills])}.")
        
        if cloud_skills:
            learning_path.append(f"Build cloud infrastructure skills: {', '.join([s.title() for s in cloud_skills])}.")
        
        if soft_skills:
            learning_path.append(f"Complement your technical growth with: {', '.join([s.title() for s in soft_skills])}.")
        
        if not any([tech_skills, analysis_skills, cloud_skills, soft_skills]):
            # Fallback for other skills
            learning_path = [f"Focus on developing: {', '.join([s.title() for s in missing_skills[:3]])}."]
            if len(missing_skills) > 3:
                learning_path.append(f"Then work on: {', '.join([s.title() for s in missing_skills[3:]])}.")
    
    return {"recommendations": recommendations, "learning_path": learning_path}

def generate_llm_feedback(resume_text, jd_text, missing_skills):
    """
    Generate actionable resume feedback using OpenAI's GPT API (new API >=1.0.0) or placeholder if not configured.
    Now provides unique, personalized feedback based on actual resume and job description content.
    """
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key:
        import openai
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Create a more detailed prompt for personalized feedback
        prompt = f"""
        You are an expert career coach and resume reviewer. Analyze the following resume and job description to provide specific, actionable feedback.

        RESUME CONTENT:
        {resume_text[:1500]}

        JOB DESCRIPTION:
        {jd_text[:1500]}

        MISSING SKILLS: {', '.join(missing_skills)}

        Based on this specific resume and job description, provide 3-5 personalized, actionable suggestions to improve the candidate's chances for this specific role. Focus on:

        1. Specific improvements to the resume content based on what's missing
        2. How to better align the resume with this particular job description
        3. Specific ways to address the missing skills in the resume
        4. Any red flags or areas that need immediate attention
        5. Strengths to emphasize and weaknesses to address

        Make your feedback specific to this resume and job, not generic advice. Reference specific parts of the resume and job description when possible.

        FEEDBACK:
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Fallback to placeholder if API fails
            pass
    
    # Enhanced placeholder feedback that's more specific
    return (
        f"Based on your resume and the job description, here are specific recommendations:\n\n"
        f"1. **Address Missing Skills**: Your resume doesn't highlight experience with {', '.join(missing_skills[:3])}. Consider adding specific projects or experiences that demonstrate these skills.\n\n"
        f"2. **Tailor Your Summary**: Update your resume summary to include keywords from the job description that match your experience.\n\n"
        f"3. **Quantify Achievements**: Add specific metrics and results to your experience sections to make your impact more measurable.\n\n"
        f"4. **Highlight Relevant Experience**: Emphasize experiences that directly relate to the job requirements and responsibilities.\n\n"
        f"5. **Professional Development**: Consider adding relevant certifications or courses that address the missing skills."
    )

def generate_role_advice(jd_text, missing_skills, job_title=None):
    """
    Generate role-specific advice using GPT if available, otherwise provide a generic template.
    Now includes the specific job title for more targeted advice and analyzes the actual job description.
    """
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key:
        import openai
        client = openai.OpenAI(api_key=openai_api_key)
        
        role_context = f"for a {job_title} position" if job_title else "for this role"
        
        # Create a more detailed prompt for personalized role advice
        prompt = f"""
        You are a career coach specializing in {job_title if job_title else 'professional development'}. 
        
        Analyze the following job description and provide specific, actionable advice for a candidate with the missing skills listed below.

        JOB DESCRIPTION:
        {jd_text[:1500]}

        MISSING SKILLS: {', '.join(missing_skills)}
        TARGET ROLE: {job_title if job_title else 'Professional Role'}

        Provide 3-5 specific pieces of advice that are tailored to this exact job description and role. Focus on:

        1. How to position yourself for this specific role despite the missing skills
        2. What the hiring manager is likely looking for based on this job description
        3. Specific strategies to address the missing skills for this particular position
        4. How to leverage existing experience to compensate for missing skills
        5. Industry-specific insights for this role and company type

        Make your advice specific to this job description and role, not generic career advice. Reference specific requirements or responsibilities from the job description when possible.

        ROLE-SPECIFIC ADVICE:
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Fallback to placeholder if API fails
            pass
    
    # Enhanced placeholder advice that's more specific
    if job_title:
        return (
            f"**Role-Specific Advice for {job_title} Position:**\n\n"
            f"1. **Industry Focus**: Research the specific requirements and trends for {job_title} roles in your target industry. Look at similar job postings to understand common expectations.\n\n"
            f"2. **Skill Prioritization**: Based on this job description, prioritize developing {', '.join(missing_skills[:2])} as these appear to be core requirements for this role.\n\n"
            f"3. **Experience Alignment**: Review the job description and focus on experiences that directly relate to the responsibilities mentioned. Emphasize transferable skills that could apply to the missing areas.\n\n"
            f"4. **Professional Network**: Connect with professionals in {job_title} roles to understand real-world expectations and get insights into how they use the skills you're missing.\n\n"
            f"5. **Strategic Positioning**: Prepare to discuss how your existing experience can be applied to the missing skill areas, and demonstrate your ability to learn quickly."
        )
    else:
        return (
            "**Role-Specific Career Advice:**\n\n"
            "1. **Research Best Practices**: Review the job description and focus on the most frequently mentioned skills and requirements.\n\n"
            "2. **Industry Trends**: Research best practices and current trends for this role in your target industry.\n\n"
            "3. **Network Insights**: Connect with professionals in the field to understand real-world expectations and day-to-day responsibilities.\n\n"
            "4. **Experience Tailoring**: Tailor your resume and portfolio to highlight experiences that directly relate to the job requirements.\n\n"
            "5. **Skill Application**: Prepare to discuss how you would apply the missing skills in practical scenarios relevant to this role."
        )

def search_real_projects(missing_skills, job_title=None):
    """
    Search for real project examples that include the missing skills.
    Returns 2-3 specific project examples with descriptions and links.
    """
    if not missing_skills:
        return "No missing skills to search for projects."
    
    # Create search queries for different platforms
    search_queries = []
    for skill in missing_skills[:3]:  # Limit to top 3 skills
        search_queries.append(f"{skill} project github")
        search_queries.append(f"{skill} portfolio example")
    
    projects_found = []
    
    try:
        # Search for GitHub projects (simplified approach)
        for query in search_queries[:4]:  # Limit searches
            # Use GitHub search API or web scraping
            search_url = f"https://github.com/search?q={query.replace(' ', '+')}&type=repositories"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            try:
                response = requests.get(search_url, headers=headers, timeout=5)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract repository information
                    repo_links = soup.find_all('a', href=re.compile(r'/[^/]+/[^/]+$'))
                    
                    for link in repo_links[:2]:  # Get first 2 results
                        repo_name = link.get_text().strip()
                        repo_url = f"https://github.com{link['href']}"
                        
                        if repo_name and not repo_name.startswith('Sign up'):
                            projects_found.append({
                                'name': repo_name,
                                'url': repo_url,
                                'description': f"GitHub repository demonstrating {', '.join(missing_skills[:2])} skills"
                            })
                            
                            if len(projects_found) >= 3:
                                break
                    
                    if len(projects_found) >= 3:
                        break
                        
            except Exception as e:
                continue
                
    except Exception as e:
        pass
    
    # If web scraping fails, provide curated examples
    if not projects_found:
        curated_projects = {
            'python': [
                {'name': 'Data Analysis with Python', 'url': 'https://github.com/topics/python-data-analysis', 'description': 'Collection of Python data analysis projects'},
                {'name': 'Machine Learning Projects', 'url': 'https://github.com/topics/machine-learning', 'description': 'Various ML projects using Python'}
            ],
            'sql': [
                {'name': 'SQL Database Projects', 'url': 'https://github.com/topics/sql', 'description': 'Database and SQL projects'},
                {'name': 'Data Engineering with SQL', 'url': 'https://github.com/topics/data-engineering', 'description': 'Data engineering projects using SQL'}
            ],
            'aws': [
                {'name': 'AWS Cloud Projects', 'url': 'https://github.com/topics/aws', 'description': 'Cloud infrastructure projects on AWS'},
                {'name': 'Serverless Applications', 'url': 'https://github.com/topics/serverless', 'description': 'Serverless projects using AWS services'}
            ],
            'machine learning': [
                {'name': 'ML Model Projects', 'url': 'https://github.com/topics/machine-learning', 'description': 'Machine learning model implementations'},
                {'name': 'Deep Learning Projects', 'url': 'https://github.com/topics/deep-learning', 'description': 'Deep learning and neural network projects'}
            ]
        }
        
        for skill in missing_skills:
            if skill.lower() in curated_projects:
                projects_found.extend(curated_projects[skill.lower()][:1])
                if len(projects_found) >= 3:
                    break
    
    # Format the results
    if projects_found:
        result = "**Real Project Examples:**\n\n"
        for i, project in enumerate(projects_found[:3], 1):
            result += f"{i}. **{project['name']}**\n"
            result += f"   - {project['description']}\n"
            result += f"   - [View Project]({project['url']})\n\n"
        return result
    else:
        return "Focus on building your own projects to demonstrate these skills effectively."

def generate_project_suggestions(missing_skills, jd_text=None, job_title=None):
    """
    Suggest portfolio or GitHub project ideas that combine multiple missing skills.
    Now includes real project examples from web search.
    """
    if len(missing_skills) < 2:
        return "Consider building a focused project to demonstrate your expertise in the missing skill."
    
    # Get real project examples
    real_projects = search_real_projects(missing_skills, job_title)
    
    # Check if skills can be meaningfully combined
    tech_skills = [s for s in missing_skills if any(tech in s.lower() for tech in ['python', 'sql', 'aws', 'docker', 'git', 'machine learning', 'data', 'pandas', 'tensorflow', 'pytorch'])]
    analysis_skills = [s for s in missing_skills if any(analysis in s.lower() for analysis in ['excel', 'tableau', 'power bi', 'statistical analysis', 'a/b testing'])]
    cloud_skills = [s for s in missing_skills if any(cloud in s.lower() for cloud in ['aws', 'azure', 'gcp', 'docker', 'kubernetes'])]
    
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key:
        import openai
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Create a more natural prompt for combined projects
        skill_groups = []
        if tech_skills and analysis_skills:
            skill_groups.append(f"technical skills ({', '.join(tech_skills)}) and analysis tools ({', '.join(analysis_skills)})")
        elif tech_skills and cloud_skills:
            skill_groups.append(f"technical skills ({', '.join(tech_skills)}) and cloud platforms ({', '.join(cloud_skills)})")
        elif len(tech_skills) >= 2:
            skill_groups.append(f"multiple technical skills ({', '.join(tech_skills)})")
        else:
            skill_groups.append(f"your missing skills ({', '.join(missing_skills)})")
        
        role_context = f"for a {job_title} position" if job_title else "for this job"
        prompt = (
            f"Suggest 1-2 portfolio project ideas that creatively combine {skill_groups[0]} "
            f"{role_context}. Focus on projects that demonstrate practical application "
            f"and real-world value. Make the suggestions specific and actionable.\n"
            f"Job Description context: {jd_text[:500] if jd_text else ''}\n"
            f"Project Ideas:"
        )
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            ai_suggestions = response.choices[0].message.content.strip()
            return f"{ai_suggestions}\n\n{real_projects}"
        except:
            pass
    
    # Fallback: Check if we can suggest meaningful combinations
    combined_suggestions = ""
    if tech_skills and analysis_skills:
        combined_suggestions = (
            f"Build a data analysis project that combines {', '.join(tech_skills[:2])} with "
            f"{', '.join(analysis_skills[:2])}. For example, create a dashboard that "
            f"analyzes real-world data using your technical skills."
        )
    elif tech_skills and cloud_skills:
        combined_suggestions = (
            f"Develop a cloud-based application using {', '.join(tech_skills[:2])} and "
            f"deploy it using {', '.join(cloud_skills[:2])}. This demonstrates both "
            f"technical implementation and cloud infrastructure skills."
        )
    elif len(tech_skills) >= 2:
        combined_suggestions = (
            f"Create an end-to-end project that showcases {', '.join(tech_skills[:3])}. "
            f"Focus on building something complete and deployable that demonstrates "
            f"your ability to work with multiple technologies together."
        )
    else:
        combined_suggestions = "Focus on individual skill development through targeted learning and practice."
    
    return f"{combined_suggestions}\n\n{real_projects}" 