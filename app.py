import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import re
import os
import base64


query_params = st.query_params

if "user" in query_params and "role" in query_params:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = True
        st.session_state.current_user = query_params["user"]
        st.session_state.user_role = query_params["role"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None

if not st.session_state.logged_in:
    with st.sidebar:
        selected = option_menu("Main Menu", ["Login", "Register"], icons=["box-arrow-in-right", "person-plus"],
                               menu_icon="cast", orientation="vertical",
                               styles={"nav-link-selected": {
                                   "background-color": "#9D8A7C",
                                   "color": "white",
                                   "border-radius": "8px"}})

    if selected == "Login":
        st.markdown("""
                    <style>
                        .big-title {
                            font-size: 36px !important;
                            text-align: center;
                            color: #9D8A7C;
                            font-weight: bold;
                        }
                        .small-subtitle {
                            font-size: 18px !important;
                            text-align: center;
                            color: #666;
                        }
                        .stButton>button {background-color: #9D8A7C; color: black; width: 100%; border-radius: 10px;}
                        div[data-baseweb="input"]:focus-within{border-color: #9D8A7C !important;}
                    </style>
                """, unsafe_allow_html=True)

        st.markdown('<p class="big-title">Login</p>', unsafe_allow_html=True)
        st.markdown('<p class="small-subtitle">Fill details to login</p>', unsafe_allow_html=True)
        name = st.text_input("Enter username")
        password = st.text_input("Password", type="password")

        df = pd.read_csv("reg_data.csv")
        if st.button("Login"):
            if not name or not password:
                st.error("Please enter both name and password.")
            elif ((df["name"] == name) & (df['password'] == password)).any():
                user_role = df.loc[(df["name"] == name) & (df["password"] == password), "user_role"].values[0]
                st.session_state.logged_in = True
                st.session_state.current_user = name
                st.session_state.user_role = user_role
                query_params["user"] = name
                query_params["role"] = user_role

                st.success(f"Login successful! Welcome back, {name}.")
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")

    elif selected == "Register":
        st.markdown("""
                                <style>
                                    .big-title {
                                        font-size: 36px !important;
                                        text-align: center;
                                        color: #9D8A7C;
                                        font-weight: bold;
                                    }
                                    .small-subtitle {
                                        font-size: 18px !important;
                                        text-align: center;
                                        color: #666;
                                    }
                                    .stButton>button {background-color: #9D8A7C; color: black; width: 100%; border-radius: 10px;}
                                    div[data-baseweb="input"]:focus-within{border-color: #9D8A7C !important;}
                                </style>
                            """, unsafe_allow_html=True)

        st.markdown('<p class="big-title">Register</p>', unsafe_allow_html=True)
        st.markdown('<p class="small-subtitle">Fill details to Sign-Up</p>', unsafe_allow_html=True)
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        user_role = st.selectbox("User Role", ["Job-Seeker", "Employer"])

        df = pd.read_csv("reg_data.csv")
        if st.button("Register"):
            if name in df["name"].values:
                st.error("Username already taken. Choose another.")
            elif not name or not email or not password or not user_role:
                st.error("All fields are required!")
            elif not email.endswith("@gmail.com") or "@" not in email:
                st.error("Please enter a valid Gmail address (example@gmail.com)")
            elif len(password) < 8 or not any(char.isdigit() for char in password) or not any(
                    char in "!@#$%^&*()-+=<>?/" for char in password):
                st.error("Password must be at least 8 characters long and include at least one number and one special character (!@#$%^&*()-+=<>?/)")
            else:
                with open("reg_data.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([name, email, password, user_role])
                st.success(f"Registration successful! Welcome, {name}!")

if st.session_state.logged_in and st.session_state.user_role:
    with st.sidebar:
        if st.session_state.user_role == "Job-Seeker":
            selected = option_menu("Home",
                                   ["Dashboard", "Resume Upload","User Profile","Job Matching", "Recruitment Analytics","Settings", "About Us", "Log out"],
                                   icons=["cast", "folder","person","search","bar-chart","gear", "people", "box-arrow-right"],
                                   menu_icon="house", orientation="vertical",styles={"nav-link-selected": {
                                   "background-color": "#9D8A7C",
                                   "color": "white",
                                   "border-radius": "8px"}})

        elif st.session_state.user_role == "Employer":
            selected = option_menu("Home", ["Dashboard", "Job Upload", "Job Openings","Candidate Matching","Visualization","Job-Settings", "About-Us", "Log out"],
                                   icons=["cast", "briefcase", "book","search","bar-chart","gear", "people", "box-arrow-right"],
                                   menu_icon="house", orientation="vertical",styles={"nav-link-selected": {
                                   "background-color": "#9D8A7C",
                                   "color": "white",
                                   "border-radius": "8px"}})

    if st.session_state.user_role == "Job-Seeker" and selected == "Dashboard":
        st.markdown("""
                            <style>
                                .big-title {
                                    font-size: 36px !important;
                                    text-align: center;
                                    color: #9D8A7C;
                                    font-weight: bold;
                                }
                                .small-subtitle {
                                    font-size: 18px !important;
                                    text-align: center;
                                    color: #666;
                                }
                            </style>""", unsafe_allow_html=True)

        st.markdown('<p class="big-title">Welcome to TalentBloom !</p>', unsafe_allow_html=True)
        st.markdown('<p class="small-subtitle">A platform for optimized job recommendations and recruitment.</p>',unsafe_allow_html=True)
        st.markdown("----")

        st.image("https://i.pinimg.com/736x/d6/a6/92/d6a692fc1e0489955e2b4ed4ae742c76.jpg")
        st.markdown("<p class='small-subtitle'>Job-Seeker's path to achieve the Perfect Job!</p>",unsafe_allow_html=True)
        st.write(
            """
            Looking for the right job can be overwhelming, but we make it **easy, fast, and personalized** just for you!  
            TalentBloom, an **AI-powered recruitment system** which helps you to find jobs that truly match your skills and career goals.
            """)
        st.markdown("#### **What You Get:**")
        st.markdown("""
        - **Smart Job Matches** – Get job recommendations based on your skills and interests.
        - **Easy Applications** – Apply for jobs with just a few clicks.
        - **Improve Your Profile** – Get AI-based resume feedback and skill suggestions.
        - **Stay Updated** – Set alerts for new jobs and interview invites.
        """)
        st.markdown(
            """
            <style>
            .centered-title {
                text-align: center;
            }
            </style>
            <h5 class="centered-title">Start Your Job Search Today!</h5>""",unsafe_allow_html=True)


    elif selected == "Resume Upload":
        st.markdown("""
                    <style>
                        .big-title {
                            font-size: 36px !important;
                            text-align: center;
                            color: #9D8A7C;
                            font-weight: bold;
                        }
                        .small-subtitle {
                            font-size: 18px !important;
                            text-align: center;
                            color: #666;
                        }
                        .stButton>button {background-color: #9D8A7C; color: black; width: 100%; border-radius: 10px;}
                        div[data-baseweb="input"]:focus-within{border-color: #9D8A7C !important;}
                    </style>""", unsafe_allow_html=True)

        st.markdown('<p class="big-title">Resume Registration</p>', unsafe_allow_html=True)
        st.markdown('<p class="small-subtitle">Fill details to get the best job recommendations</p>',unsafe_allow_html=True)
        st.markdown("----")

        resumes_folder = "resumes"
        os.makedirs(resumes_folder, exist_ok=True)
        form_data_path = "form_data.csv"

        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number", placeholder="+91 0123456789")
        age = st.number_input("Age", min_value=18, max_value=65)
        education = st.selectbox(" Highest Education Level",
                                 ["High School", "Bachelor's", "Master's", "PhD", "Other"])
        skills = st.selectbox("Choose Your Skills",
                              ["AI-ML Algorithms/Data Processing/NLP/Deep Learning", "Java", "Python", "JavaScript(React.js/Angular/Node.js)", "HTML/CSS",
                               "UI/UX(Figma)/Designing","MySQL/NoSQL/SQLite/Node.js","Data Visualization(Pandas & NumPy)/Statistics","Data Analysis/ Business Intelligence"])
        experience = st.number_input("Years of Work Experience", min_value=0, max_value=50)
        industry = st.selectbox("Preferred Job Role",
                                ["Machine Learning / AI Engineer", "Web Development (Frontend)",
                                 "Web Development (Backend)", "Full-Stack Developer","Data Science / Data Analyst", "Database Management",
                                 "Business Analyst","UI/UX Designer"])
        linkedin = st.text_input("LinkedIn link")
        github = st.text_input("GitHub link")
        projects = st.text_area("Projects", placeholder="Briefly mention your key projects")
        uploaded_resume = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

        if os.path.exists(form_data_path):
            df = pd.read_csv(form_data_path)
        else:
            df = pd.DataFrame(columns=[
                "name", "email", "phone", "age", "education", "skills", "experience",
                "industry", "projects", "linkedin", "github", "resume"
            ])

        if st.button("Submit"):
            if not name or not email or not phone or not skills or not industry or not uploaded_resume:
                st.error("All fields including resume upload are required!")
            elif name in df["name"].values:
                st.error("Username already taken. Choose another.")
            elif not email.endswith("@gmail.com") or "@" not in email:
                st.error("Please enter a valid Gmail address (example@gmail.com)!")
            else:

                safe_name = name.strip().replace(" ", "_").lower()
                resume_filename = f"{safe_name}_resume.pdf"
                resume_path = os.path.join(resumes_folder, resume_filename)
                with open(resume_path, "wb") as f:
                    f.write(uploaded_resume.read())

                new_entry = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "age": age,
                    "education": education,
                    "skills": skills,
                    "experience": experience,
                    "industry": industry,
                    "projects": projects,
                    "linkedin": linkedin,
                    "github": github,
                    "resume": resume_filename
                }
                df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
                df.to_csv(form_data_path, index=False)

                st.session_state.user_profile_data = new_entry
                st.success(f"✅ Uploaded successfully! Welcome, {name}!")

    elif selected == "User Profile":
        st.markdown("""
                            <style>
                                .big-title {
                                    font-size: 36px !important;
                                    text-align: center;
                                    color: #9D8A7C;
                                    font-weight: bold;
                                }
                                .small-subtitle {
                                    font-size: 18px !important;
                                    text-align: center;
                                    color: #666;
                                }
                            </style>""", unsafe_allow_html=True)

        st.markdown('<p class="big-title">Your Profile</p>', unsafe_allow_html=True)
        st.markdown('<p class="small-subtitle">Matching jobs based on your resume and job-requirements.</p>',unsafe_allow_html=True)
        st.markdown("----")

        if "user_profile_data" in st.session_state:
            data = st.session_state.user_profile_data
            st.write(f"**Name:** {data['name']}")
            st.write(f"**Email:** {data['email']}")
            st.write(f"**Skills:** {data['skills']}")
            st.write(f"**Experience:** {data['experience']} years")
            st.write(f"**Job Role:** {data['industry']}")
            st.write(f"**LinkedIn Link:** {data['linkedin']}")
            st.write(f"**GitHub Link:** {data['github']}")
            st.write(f"**Projects:** {data['projects']}")

            if data["resume"]:
                st.download_button("Download Resume",
                                   data=data["resume"].getvalue(),
                                   file_name="resume.pdf",
                                   mime="application/pdf")

            st.markdown("---")

            job_data = pd.read_csv("employer_data.csv")
            resume_data = pd.read_csv("form_data.csv")
            job_data.fillna("", inplace=True)
            resume_data.fillna("", inplace=True)
            job_data["combined"] = job_data["Title"] + " " + job_data["Skills"] + " " + job_data["Experience"].astype(str)
            user_resume_text = data["industry"] + " " + " ".join(data["skills"]) + " " + str(data["experience"])
            resume_data = pd.DataFrame([data])
            resume_data["combined"] = user_resume_text
            vectorizer = TfidfVectorizer()
            job_vectors = vectorizer.fit_transform(job_data["combined"])
            resume_vector = vectorizer.transform([user_resume_text])
            similarity_scores = cosine_similarity(job_vectors, resume_vector).flatten()
            job_data["Match Score"] = similarity_scores
            job_data = job_data[job_data["Match Score"] > 0].sort_values(by="Match Score", ascending=False).head(10)
            if not job_data.empty:
                st.markdown('<p class="small-subtitle">Suggested Jobs.</p>',unsafe_allow_html=True)
                cols = st.columns(2)
                for i, (_, job) in enumerate(job_data.iterrows()):
                    with cols[i % 2]:
                        st.markdown(f"""
                        <div style='border:1px solid #ccc; border-radius:10px; padding:15px; margin-bottom:20px ; box-shadow: 2px 2px 8px rgba(0,0,0,0.05);'>
                        <h4 style='margin-bottom:5px;'>{job['Company']}</h4>
                        <p><b>Title:</b> {job['Title']}</p>
                        <p><b>Email:</b> {job['Email']}</p>
                        <p><b>Website:</b> {job['Website']}</p>
                        <p><b>Location:</b> {job['Location']}</p>
                        <p><b>Experience:</b> {job['Experience']} years</p>
                        <p><b>Skills:</b> {job['Skills']}</p>
                        <p><b>Salary:</b> {job['Salary']}</p>
                        <p><b>Type:</b> {job['Type']}</p>
                        </div>""", unsafe_allow_html=True)
            else:
                st.info("No matching jobs found based on your resume.")
        else:
            st.warning("Please upload your resume in the 'Resume Upload' tab.")


    elif selected == "Job Matching":
        st.markdown("""
                    <style>
                        .big-title {
                            font-size: 36px !important;
                            text-align: center;
                            color: #9D8A7C;
                            font-weight: bold;
                        }
                        .small-subtitle {
                            font-size: 18px !important;
                            text-align: center;
                            color: #666;
                        }
                    </style>""", unsafe_allow_html=True)

        st.markdown('<p class="big-title">Job Matching</p>', unsafe_allow_html=True)
        st.markdown('<p class="small-subtitle">Matching jobs based on skills.</p>', unsafe_allow_html=True)
        st.markdown("----")

        job_data = pd.read_csv("employer_data.csv")
        resume_data = pd.read_csv("form_data.csv")

        job_data.fillna("", inplace=True)
        resume_data.fillna("", inplace=True)

        job_data["combined"] = job_data["Title"] + " " + job_data["Skills"] + " " + job_data["Experience"].astype(str)
        resume_data["combined"] = resume_data["industry"] + " " + resume_data["skills"] + " " + resume_data["experience"].astype(str)

        vectorizer = TfidfVectorizer()
        job_vectors = vectorizer.fit_transform(job_data["combined"])
        resume_vectors = vectorizer.transform(resume_data["combined"])

        similarity_matrix = cosine_similarity(job_vectors, resume_vectors)
        selected_skills_jobseeker = st.multiselect("Select Your Skills", resume_data["skills"].unique())

        if st.button("Find Matching Jobs"):
            matching_candidates = resume_data[resume_data["skills"].isin(selected_skills_jobseeker)]
            if matching_candidates.empty:
                st.write("Need to select atleast one skill(s).")
            else:
                matching_indices = matching_candidates.index.tolist()
                similar_jobs = similarity_matrix[:, matching_indices].mean(axis=1)
                sorted_jobs = sorted(enumerate(similar_jobs), key=lambda x: x[1], reverse=True)

                st.write("### Matching Jobs:")
                for idx, score in sorted_jobs[:25]:
                    job = job_data.iloc[idx]
                    st.write(f"**Company:** {job['Company']}")
                    st.write(f"**Email:** {job['Email']}")
                    st.write(f"**Website:** {job['Website']}")
                    st.write(f"**Job Title:** {job['Title']}")
                    st.write(f"**Location:** {job['Location']}")
                    st.write(f"**Experience Required:** {job['Experience']} years")
                    st.write(f"**Skills Required:** {job['Skills']}")
                    st.write(f"**Salary:** {job['Salary']}")
                    st.write(f"**Job Type:** {job['Type']}")
                    st.write("---")


    elif selected == "Recruitment Analytics":

        st.markdown("""
                            <style>
                                .big-title {
                                    font-size: 36px !important;
                                    text-align: center;
                                    color: #9D8A7C;
                                    font-weight: bold;
                                }
                                .small-subtitle {
                            font-size: 20px !important;
                            text-align: center;
                            color: #666;
                        }
                            </style>
                        """, unsafe_allow_html=True)

        st.markdown('<p class="big-title">Recruitment Analytics</p>', unsafe_allow_html=True)
        st.markdown("----")
        st.markdown('<p class="small-subtitle">Skill Analytics.</p>', unsafe_allow_html=True)

        data = pd.read_csv("form_data.csv")
        df = pd.DataFrame(data)
        fig = px.pie(df, names="skills", title="Available Skills", hole=0.3,
                     labels={"skills": "Skills"},
                     color_discrete_sequence=px.colors.qualitative.Set3,
                     template="plotly_white")
        st.plotly_chart(fig)


        st.markdown('<p class="small-subtitle">Skill-Based Job Opportunities.</p>', unsafe_allow_html=True)
        selected_skill = st.selectbox("Select a Skill:", df["skills"].unique())
        filtered_df = df[df["skills"] == selected_skill]
        industry_counts = filtered_df["industry"].value_counts().reset_index()
        industry_counts.columns = ["Industry", "Job Count"]

        fig = px.bar(
            industry_counts,
            x="Industry",
            y="Job Count",
            title=f"Job Opportunities for {selected_skill}",
            labels={"Industry": "Industry", "Job Count": "Number of Jobs"},
            color="Job Count",
        )
        st.plotly_chart(fig)
        st.markdown("---")

        df = pd.read_csv("form_data.csv")
        df_exploded = df.assign(skills=df['skills'].str.split(',')).explode('skills')
        skill_counts = df_exploded['skills'].value_counts().reset_index()
        skill_counts.columns = ['Skill', 'Count']
        skill_counts = skill_counts.sort_values(by="Count", ascending=True)
        fig = px.line(skill_counts, x='Count', y='Skill', title='Skills Demand Rate', markers=True,
                      labels={'Skill': 'Skill', 'Count': 'Number of Candidates'})
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("---")

        st.markdown('<p class="small-subtitle">Skill-Based Job Paying.</p>', unsafe_allow_html=True)
        df = pd.read_csv("employer_data.csv")
        def clean_salary(salary):
            if pd.isna(salary):
                return 0
            salary = re.sub(r"[^\d]", "", str(salary))
            return int(salary) if salary else 0
        df["Salary"] = df["Salary"].apply(clean_salary)
        all_skills = set()
        df["Skills"].dropna().apply(lambda x: all_skills.update([s.strip() for s in x.split(",")]))  # Split skills
        selected_skill = st.selectbox("Select a Skill:", sorted(all_skills))
        escaped_skill = re.escape(selected_skill)
        filtered_df = df[df["Skills"].str.contains(fr"\b{re.escape(selected_skill)}\b", case=False, na=False)]
        total_jobs = len(filtered_df)
        st.metric(label=f"Total Jobs for {selected_skill}", value=total_jobs)
        if not filtered_df.empty:
            filtered_df = filtered_df.sort_values(by="Salary", ascending=False)
            fig = px.bar(
                filtered_df,
                x="Title",
                y="Salary",
                color="Company",
                barmode="group",
                title=f"Salary Distribution for {selected_skill}",
                labels={"Title": "Job Title", "Salary": "Salary", "Company": "Company"},
            )
            st.plotly_chart(fig)
        else:
            st.write(f"No jobs found for the skill: {selected_skill}")



        st.markdown('<p class="small-subtitle">Job Analytics.</p>', unsafe_allow_html=True)
        data = pd.read_csv("employer_data.csv")
        df = pd.DataFrame(data)
        fig = px.pie(df, names="Title", title="Total Available Job-fields ", hole=0.3,
                     labels={"Title": "Job-Field"},
                     color_discrete_sequence=px.colors.qualitative.Set3,
                     template="plotly_white")
        st.plotly_chart(fig)


        st.markdown('<p class="small-subtitle">Skill-Highest Choosen Job-Fields.</p>', unsafe_allow_html=True)
        df = pd.read_csv("form_data.csv")
        industry_counts = df["industry"].value_counts().reset_index()
        industry_counts.columns = ["industry", "Job Seekers"]
        industry_counts = industry_counts.sort_values(by="Job Seekers", ascending=False)
        fig = px.bar(
            industry_counts,
            y="industry",
            x="Job Seekers",
            text="Job Seekers",
            orientation='h',
            title="Industries Chosen by Job Seekers (Highest to Lowest)",
            labels={"industry": "Industry", "Job Seekers": "Number of Job Seekers"},
            color="Job Seekers",
        )
        st.plotly_chart(fig)

    elif selected == "Settings":
        st.markdown("""
                    <style>
                        .big-title {
                            font-size: 36px !important;
                            text-align: center;
                            color: #9D8A7C;
                            font-weight: bold;
                        }
                        .small-subtitle {
                            font-size: 18px !important;
                            text-align: center;
                            color: #666;
                        }
                        .stButton>button {background-color: #9D8A7C; color: black; width: 100%; border-radius: 10px;}
                        div[data-baseweb="input"]:focus-within{border-color: #9D8A7C !important;}
                    </style>""", unsafe_allow_html=True)

        st.markdown('<p class="big-title">Settings</p>', unsafe_allow_html=True)
        st.markdown('<p class="small-subtitle">Update Your Profile</p>',unsafe_allow_html=True)
        st.markdown("----")

        form_data_path = "form_data.csv"

        if not os.path.exists(form_data_path):
            st.warning("No user data found.")
            st.stop()

        df = pd.read_csv(form_data_path)
        name_to_edit = st.text_input("Enter your registered Full-Name to edit your details")

        if name_to_edit:
            if name_to_edit not in df['name'].values:
                st.error("Name not found in records. Make sure you are using the one used for registration.")
            else:
                idx = df[df['name'] == name_to_edit].index[0]
                user_data = df.loc[idx]

                email = st.text_input("Email Address", user_data['email'])
                phone = st.text_input("Phone Number", user_data['phone'])
                age = st.number_input("Age", min_value=18, max_value=65, value=int(user_data['age']))
                education = st.selectbox("Highest Education Level",
                                         ["High School", "Bachelor's", "Master's", "PhD", "Other"],
                                         index=["High School", "Bachelor's", "Master's", "PhD", "Other"].index(
                                             user_data['education']))
                skills = st.text_input("Skills", user_data['skills'])
                experience = st.number_input("Experience (Years)", min_value=0, max_value=50,
                                             value=int(user_data['experience']))
                industry = st.text_input("Preferred Job Role", user_data['industry'])
                projects = st.text_area("Projects", user_data['projects'])
                linkedin = st.text_input("LinkedIn", user_data['linkedin'])
                github = st.text_input("GitHub", user_data['github'])

                if st.button("Save Changes"):
                    df.loc[idx, 'email'] = email
                    df.loc[idx, 'phone'] = phone
                    df.loc[idx, 'age'] = age
                    df.loc[idx, 'education'] = education
                    df.loc[idx, 'skills'] = skills
                    df.loc[idx, 'experience'] = experience
                    df.loc[idx, 'industry'] = industry
                    df.loc[idx, 'projects'] = projects
                    df.loc[idx, 'linkedin'] = linkedin
                    df.loc[idx, 'github'] = github

                    df.to_csv(form_data_path, index=False)
                    st.success("Profile updated successfully!")


    elif selected == "About Us":
        st.markdown("""
                <style>
                    .big-title {
                        font-size: 36px !important;
                        text-align: center;
                        color: #9D8A7C;
                        font-weight: bold;
                    }
                </style>""", unsafe_allow_html=True)

        st.markdown('<p class="big-title">About Us</p>', unsafe_allow_html=True)
        st.markdown("----")

        st.subheader("Welcome to TalentBloom")
        st.write(
            "The TalentBloom is an AI-Driven Resume and Job Matching System for Optimal Talent Acquisition is designed to enhance the recruitment process by intelligently connecting candidates with the most relevant job opportunities. Utilizing advanced machine learning algorithms and natural language processing, the system analyzes job requirements and candidate profiles to identify the best-fit opportunities. By leveraging data-driven insights and predictive analytics, it ensures a seamless and efficient hiring experience for both employers and job seekers. This system optimizes talent acquisition by fostering meaningful connections, reducing hiring complexities, and improving overall workforce alignment.")

        st.subheader("Our Motto")
        st.write("""
        We aim to **bridge the gap between talent and opportunity** by offering :
        - Personalized job recommendations based on user roles.
        - A seamless and interactive job application process.
        - Future enhancements like resume uploads and application tracking.
        - To automate and optimize the recruitment process using AI-driven algorithms. 
        - To provide accurate job recommendations for candidates based on their profiles. 
        - To minimize bias and increase fairness in the recruitment process.
        """)

        st.subheader("Why Choose Us?")
        st.write("""
        - **Role-Based Filtering** – Get job listings that match your skills.  
        - **User-Friendly Interface** – Easily apply for jobs with a single click.  
        - **Expanding Features** – Future updates include user authentication and saved applications.  
        - **Remote & On-Site Jobs** – Browse opportunities from various industries.  
        """)

        st.subheader("Future Enhancements")
        st.write("""
        - **User Authentication** – Create an account to save applications.  
        - **Resume Upload** – Apply directly with your resume.  
        - **AI-Powered Recommendations** – Smart job suggestions based on skills & experience.  
        """)

        st.subheader("Contact Us")
        st.write("""
        - **Email:** talentbloom@gmail.com  
        - **Website:** [www.talentbloom.com](#)  
        - **Location:** Ahmedabad  
        """)

        st.write(" **Join us in shaping the future better!** ")

    if st.session_state.user_role == "Employer" and selected == "Dashboard":
        st.markdown("""
                        <style>
                            .big-title {
                                font-size: 36px !important;
                                text-align: center;
                                color: #9D8A7C;
                                font-weight: bold;
                            }
                            .small-subtitle {
                                font-size: 18px !important;
                                text-align: center;
                                color: #666;
                            }
                        </style>""", unsafe_allow_html=True)

        st.markdown('<p class="big-title">Welcome to TalentBloom !</p>', unsafe_allow_html=True)
        st.markdown('<p class="small-subtitle">A platform for Hire Smarter with AI-Powered Recruitment.</p>',unsafe_allow_html=True)
        st.markdown("----")

        st.image("https://i.pinimg.com/736x/d6/a6/92/d6a692fc1e0489955e2b4ed4ae742c76.jpg")
        st.markdown("<p class='small-subtitle'>Employer's path for Perfect Hiring!</p>", unsafe_allow_html=True)
        st.write(
            "TalentBloom,a platform that helps employers like you to find the right talent efficiently using AI-driven matching. "
            "Post jobs, screen candidates, and make data-driven hiring decisions—all in one place!")

        st.markdown("#### **Key Features for Employers**")
        st.markdown(
            """
            - **Post Jobs Effortlessly**: Create job listings with AI-suggested descriptions.
            - **Get Matched with the Best Candidates**: AI-powered screening for role-based hiring.
            - **Manage Applications Seamlessly**: Track applicants from application to hiring.
            - **AI-Powered Candidate Insights**: View suitability scores and skill gap analysis.
            - **Efficient Communication & Scheduling**: Contact candidates and schedule interviews.
            - **Data-Driven Hiring Decisions**: Get recruitment analytics and market insights.
            """
        )
        st.markdown(
            """
            <style>
            .centered-title {
                text-align: center;
            }
            </style>
            <h5 class="centered-title">Start Hiring Smarter Today! Post your job.</h5>""", unsafe_allow_html=True)

    elif selected == "Job Upload":
        st.markdown("""
                                <style>
                                    .big-title {
                                        font-size: 36px !important;
                                        text-align: center;
                                        color: #9D8A7C;
                                        font-weight: bold;
                                    }
                                    .small-subtitle {
                                        font-size: 18px !important;
                                        text-align: center;
                                        color: #666;
                                    }
                                    .stButton>button {background-color: #9D8A7C; color: black; width: 100%; border-radius: 10px;}
                                    div[data-baseweb="input"]:focus-within{border-color: #9D8A7C !important;}
                                </style>
                            """, unsafe_allow_html=True)

        st.markdown('<p class="big-title">Job Posting</p>', unsafe_allow_html=True)
        st.markdown('<p class="small-subtitle">Fill details to upload a new job</p>', unsafe_allow_html=True)
        st.markdown("----")

        # Input fields
        name = st.text_input("Name")
        job_title = st.selectbox("Preferred Job Role",
                                ["Machine Learning / AI Engineer", "Web Development (Frontend)",
                                 "Web Development (Backend)", "Full-Stack Developer","Data Science / Data Analyst", "Database Management",
                                 "Business Analyst","UI/UX Designer"])
        company = st.text_input("Company Name")
        email = st.text_input("Email Address")
        website = st.text_input("Website")
        location = st.text_input("Location")
        experience = st.number_input("Experience Required (Years)", min_value=0, max_value=50)
        skills = st.selectbox("Choose Your Skills",
                              ["AI-ML Algorithms/Data Processing/NLP/Deep Learning", "Java", "Python", "JavaScript(React.js/Angular/Node.js)", "HTML/CSS",
                               "UI/UX(Figma)/Designing","MySQL/NoSQL/SQLite/Node.js","Data Visualization(Pandas & NumPy)/Statistics","Data Analysis/ Business Intelligence"])
        salary = st.text_input("Salary")
        job_type = st.selectbox(" Job Type", ["Full-Time", "Part-Time", "Internship", "Contract"])

        if st.button("Post Job"):
            if not name or not job_title or not company or not email or not website or not location or not experience or not skills or not salary or not job_type:
                st.error("All fields are required!")
            else:
                with open("employer_data.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([name, job_title, company, location, experience, skills, salary, job_type])
                st.success(f"Job Uploaded Successfully!")

    elif selected == "Job Openings":
        st.markdown("""
                        <style>
                            .big-title {
                                font-size: 36px !important;
                                text-align: center;
                                color: #9D8A7C;
                                font-weight: bold;
                            }
                            .small-subtitle {
                                font-size: 18px !important;
                                text-align: center;
                                color: #666;
                            }
                        </style>""", unsafe_allow_html=True)

        st.markdown('<p class="big-title">Job Openings</p>', unsafe_allow_html=True)
        st.markdown('<p class="small-subtitle">List of Jobs available in market.</p>', unsafe_allow_html=True)
        st.markdown("----")

        df = pd.read_csv("employer_data.csv")
        for idx, row in df.iterrows():
            st.subheader(f"{row['Title']} at {row['Company']}")
            st.write(f"Email: {row['Email']}")
            st.write(f"Website: {row['Website']}")
            st.write(f"Location: {row['Location']}")
            st.write(f"Experience: {row['Experience']} years")
            st.write(f"Skills: {row['Skills']}")
            st.write(f"Salary: {row['Salary']}")
            st.write(f"Type: {row['Type']}")
            st.markdown("---")


    elif  selected == "Candidate Matching":
        st.markdown("""
                        <style>
                            .big-title {
                                font-size: 36px !important;
                                text-align: center;
                                color: #9D8A7C;
                                font-weight: bold;
                            }
                            .small-subtitle {
                                font-size: 18px !important;
                                text-align: center;
                                color: #666;
                            }
                        </style>""", unsafe_allow_html=True)

        st.markdown('<p class="big-title">Candidate Matching</p>', unsafe_allow_html=True)
        st.markdown('<p class="small-subtitle">Matching candidates based on the job description.</p>', unsafe_allow_html=True)
        st.markdown("----")

        job_data = pd.read_csv("employer_data.csv")
        resume_data = pd.read_csv("form_data.csv")
        job_data.fillna("", inplace=True)
        resume_data.fillna("", inplace=True)

        job_data["combined"] = job_data["Title"] + " " + job_data["Skills"] + " " + job_data["Experience"].astype(str)
        resume_data["combined"] = resume_data["industry"] + " " + resume_data["skills"] + " " + resume_data[
            "experience"].astype(str)

        vectorizer = TfidfVectorizer()
        all_texts = pd.concat([job_data["combined"], resume_data["combined"]], axis=0)
        vectorizer.fit(all_texts)
        job_vectors = vectorizer.transform(job_data["combined"])
        resume_vectors = vectorizer.transform(resume_data["combined"])

        similarity_matrix = cosine_similarity(job_vectors, resume_vectors)

        selected_job_title = st.selectbox("Select Job Title", job_data["Title"].unique())
        selected_skills = st.multiselect("Select Skill(s)", job_data["Skills"].unique())

        if st.button("Find Matching Candidates"):
            matching_jobs = job_data[
                (job_data["Title"] == selected_job_title) & (job_data["Skills"].isin(selected_skills))]
            if matching_jobs.empty:
                st.error("No matching jobs found. Please select valid skills.")
            else:
                matching_indices = matching_jobs.index.tolist()
                similar_candidates = similarity_matrix[matching_indices].mean(axis=0)
                sorted_candidates = sorted(enumerate(similar_candidates), key=lambda x: x[1], reverse=True)

                st.write("### Eligible Candidates:")
                resume_df = pd.read_csv("form_data.csv")
                resume_df.fillna("", inplace=True)

                for idx, score in sorted_candidates[:20]:
                    candidate = resume_df.iloc[idx]

                    st.markdown(f"**Name:** {candidate['name']}")
                    st.markdown(f"**Email:** {candidate['email']}")
                    st.markdown(f"**Experience:** {candidate['experience']} years")
                    st.markdown(f"**Preferred Job Role:** {candidate['industry']}")
                    st.markdown(f"**Prediction Score:** {score:.2f}")

                    resume_filename = candidate['resume']
                    resume_path = os.path.join("resumes", resume_filename)

                    if os.path.exists(resume_path):
                        with open(resume_path, "rb") as f:
                            resume_file_data = f.read()
                            base64_pdf = base64.b64encode(resume_file_data).decode("utf-8")
                            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>'
                            st.markdown(pdf_display, unsafe_allow_html=True)

                        st.download_button(
                            label="Download Resume",
                            data=resume_file_data,
                            file_name=resume_filename,
                            mime="application/pdf"
                        )
                    else:
                        st.error(f"Resume file not found: {resume_path}")
                    st.markdown("---")

    elif selected == "Visualization":

        st.markdown("""
                            <style>
                                .big-title {
                                    font-size: 36px !important;
                                    text-align: center;
                                    color: #9D8A7C;
                                    font-weight: bold;
                                }
                                .small-subtitle {
                                font-size: 20px !important;
                                text-align: center;
                                color: #666;
                                }
                            </style>
                        """, unsafe_allow_html=True)

        st.markdown('<p class="big-title"> Visualization</p>', unsafe_allow_html=True)
        st.markdown("----")

        st.markdown('<p class="small-subtitle">Job-based Candidate Distribution.</p>', unsafe_allow_html=True)
        df = pd.read_csv("form_data.csv")
        df_exploded = df.assign(industry=df['industry'].str.split(',')).explode('industry')
        job_counts = df_exploded['industry'].value_counts().reset_index()
        job_counts.columns = ['Industry', 'Count']
        job_counts = job_counts.sort_values(by="Count", ascending=True)
        fig = px.line(job_counts, x='Count', y='Industry', title='Job(s) Demand Rate',markers=True,
                     labels={'Industry': 'Industry', 'Count': 'Number of Candidates'})
        st.plotly_chart(fig)
        st.markdown("----")


        st.markdown('<p class="small-subtitle">Skill-based Candidate Distribution.</p>',unsafe_allow_html=True)
        selected_skills_for_graph = st.multiselect("Select Skills to Visualize", df["skills"].unique())
        if selected_skills_for_graph:
            skill_counts = df[df["skills"].isin(selected_skills_for_graph)]["skills"].value_counts().reset_index()
            skill_counts.columns = ["Skill", "Candidate Count"]
            fig = px.bar(skill_counts,
                         x="Skill",
                         y="Candidate Count",
                         color="Skill",
                         title="Number of Employees per Selected Skill",)
            fig.update_layout(xaxis_title="Skill", yaxis_title="Number of Candidates")
            st.plotly_chart(fig)
        st.markdown("----")

        st.markdown('<p class="small-subtitle">Candidates sorted by Education.</p>', unsafe_allow_html=True)
        df=pd.read_csv("form_data.csv")
        fig = px.pie(df, names="education",title="Education",hole=0.3,labels={"education":"Education-Status"},color_discrete_sequence=px.colors.qualitative.Set3,template="plotly_white")
        st.plotly_chart(fig)


    elif selected == "Job-Settings":
        st.markdown("""
                    <style>
                        .big-title {
                            font-size: 36px !important;
                            text-align: center;
                            color: #9D8A7C;
                            font-weight: bold;
                        }
                        .small-subtitle {
                            font-size: 18px !important;
                            text-align: center;
                            color: #666;
                        }
                        .stButton>button {background-color: #9D8A7C; color: black; width: 100%; border-radius: 10px;}
                        div[data-baseweb="input"]:focus-within{border-color: #9D8A7C !important;}
                    </style>""", unsafe_allow_html=True)

        st.markdown('<p class="big-title">Settings</p>', unsafe_allow_html=True)
        st.markdown('<p class="small-subtitle">Update Job Profile</p>',unsafe_allow_html=True)
        st.markdown("----")

        employer_data_path = "employer_data.csv"

        if not os.path.exists(employer_data_path):
            st.warning("No user data found.")
            st.stop()

        df = pd.read_csv(employer_data_path)
        name_to_edit = st.text_input("Enter your registered Full-Name to edit your details")

        if name_to_edit:
            if name_to_edit not in df['Employer'].values:
                st.error("Name not found in records. Make sure you are using the one used for registration.")
            else:
                idx = df[df['Employer'] == name_to_edit].index[0]
                employer = df.loc[idx]

                job_title = st.selectbox("Preferred Job Role",
                                         ["Machine Learning / AI Engineer", "Web Development (Frontend)",
                                          "Web Development (Backend)", "Full-Stack Developer",
                                          "Data Science / Data Analyst", "Database Management",
                                          "Business Analyst", "UI/UX Designer"],
                                         index=["Machine Learning / AI Engineer", "Web Development (Frontend)",
                                                "Web Development (Backend)", "Full-Stack Developer",
                                                "Data Science / Data Analyst", "Database Management",
                                                "Business Analyst", "UI/UX Designer"].index(employer['Title']))
                company = st.text_input("Company Name", employer['Company'])
                email = st.text_input("Email",employer['Email'])
                website = st.text_input("Website", employer['Website'])
                location = st.text_input("Location", employer['Location'])
                experience = st.number_input("Experience Required (Years)", min_value=0, max_value=50,
                                             value=int(employer['Experience']))
                skills = st.selectbox("Choose Your Skills",
                                      ["AI-ML Algorithms/Data Processing/NLP/Deep Learning", "Java", "Python",
                                       "JavaScript(React.js/Angular/Node.js)", "HTML/CSS",
                                       "UI/UX(Figma)/Designing", "MySQL/NoSQL/SQLite/Node.js",
                                       "Data Visualization(Pandas & NumPy)/Statistics",
                                       "Data Analysis/ Business Intelligence"],
                                      index=0 if pd.isna(employer['Skills']) else 0)
                salary = st.text_input("Salary", employer['Salary'])
                job_type = st.selectbox("Job Type", ["Full-Time", "Part-Time", "Internship", "Contract"],
                                        index=["Full-Time", "Part-Time", "Internship", "Contract"].index(
                                            employer['Type']))

                if st.button("Save Changes"):

                    df.loc[idx, 'Title'] = job_title
                    df.loc[idx, 'Company'] = company
                    df.loc[idx, 'Email'] = email
                    df.loc[idx, 'Website'] = website
                    df.loc[idx, 'Location'] = location
                    df.loc[idx, 'Experience'] = experience
                    df.loc[idx, 'Skills'] = skills
                    df.loc[idx, 'Salary'] = salary
                    df.loc[idx, 'Type'] = job_type

                    df.to_csv(employer_data_path, index=False)
                    st.success("Job profile updated successfully!")

#About us (Employer)
    elif selected == "About-Us":
        st.markdown("""
                    <style>
                        .big-title {
                            font-size: 36px !important;
                            text-align: center;
                            color: #9D8A7C;
                            font-weight: bold;
                        }
                    </style>""", unsafe_allow_html=True)

        st.markdown('<p class="big-title">About Us</p>', unsafe_allow_html=True)
        st.markdown("----")

        st.subheader("Welcome to TalentBloom")
        st.write(
            "The TalentBloom is an AI-Driven Resume and Job Matching System for Optimal Talent Acquisition is designed to enhance the recruitment process by intelligently connecting candidates with the most relevant job opportunities. Utilizing advanced machine learning algorithms and natural language processing, the system analyzes job requirements and candidate profiles to identify the best-fit opportunities. By leveraging data-driven insights and predictive analytics, it ensures a seamless and efficient hiring experience for both employers and job seekers. This system optimizes talent acquisition by fostering meaningful connections, reducing hiring complexities, and improving overall workforce alignment.")

        st.subheader("Our Motto")
        st.write("""
                        We aim to **bridge the gap between talent and opportunity** by offering :
                        - Personalized job recommendations based on user roles.
                        - A seamless and interactive job application process.
                        - Future enhancements like resume uploads and application tracking.
                        - To automate and optimize the recruitment process using AI-driven algorithms. 
                        - To provide accurate job recommendations for candidates based on their profiles. 
                        - To minimize bias and increase fairness in the recruitment process.
                        """)

        st.subheader("Why Choose Us?")
        st.write("""
                        - **Role-Based Filtering** – Get job listings that match your skills.  
                        - **User-Friendly Interface** – Easily apply for jobs with a single click.  
                        - **Expanding Features** – Future updates include user authentication and saved applications.  
                        - **Remote & On-Site Jobs** – Browse opportunities from various industries.  
                        """)

        st.subheader("Future Enhancements")
        st.write("""
                        - **User Authentication** – Create an account to save applications.  
                        - **Resume Upload** – Apply directly with your resume.  
                        - **AI-Powered Recommendations** – Smart job suggestions based on skills & experience.  
                        """)

        st.subheader("Contact Us")
        st.write("""
                        - **Email:** talentbloom@gmail.com  
                        - **Website:** [www.talentbloom.com](#)  
                        - **Location:** Ahmedabad  
                        """)

        st.write(" **Join us in shaping the future better!** ")

    if selected == "Log out":
        query_params.clear()
        st.session_state.clear()
        st.rerun()