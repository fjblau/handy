import streamlit as st
import pandas as pd
from datetime import datetime, date
import json
import os
from typing import Dict, List, Any

# Page configuration
st.set_page_config(
    page_title="Handy - Goals Tracking App",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with mobile enhancements
st.markdown("""
<style>
    /* Base styles */
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    .life-area-card {
        background: #f8f9fa;
        padding: 1em;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 1em 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .goal-card {
        background: #e3f2fd;
        padding: 1em;
        border-radius: 8px;
        margin: 0.5em 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .affirmation-card {
        background: #f3e5f5;
        padding: 1em;
        border-radius: 8px;
        margin: 0.5em 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Mobile-specific styles */
    @media (max-width: 768px) {
        /* Text size adjustments */
        .main-header {
            font-size: 2em;
        }
        .sub-header {
            font-size: 1em;
        }
        
        /* Make buttons more tappable on mobile */
        button, .stButton > button {
            min-height: 44px !important;
            width: 100% !important;
            margin: 0.5em 0 !important;
        }
        
        /* Prevent zoom on input fields in iOS */
        input, textarea, select, .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            font-size: 16px !important;
        }
        
        /* Improve mobile layout */
        .row-widget.stRadio > div {
            flex-direction: column;
        }
        
        /* Adjust column layout for mobile */
        .row-widget.stHorizontal {
            flex-wrap: wrap;
        }
        
        /* Make checkboxes and radio buttons more tappable */
        .stCheckbox label, .stRadio label {
            min-height: 44px;
            display: flex;
            align-items: center;
            padding: 0.5em 0;
        }
        
        /* Adjust metrics for mobile */
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        
        /* Adjust sliders for mobile */
        .stSlider {
            padding: 1em 0 !important;
        }
        
        /* Adjust selectbox for mobile */
        .stSelectbox {
            min-height: 44px;
        }
        
        /* Adjust multiselect for mobile */
        .stMultiSelect {
            min-height: 44px;
        }
        
        /* Adjust date input for mobile */
        .stDateInput {
            min-height: 44px;
        }
        
        /* Adjust number input for mobile */
        .stNumberInput {
            min-height: 44px;
        }
        
        /* Adjust text input for mobile */
        .stTextInput {
            min-height: 44px;
        }
        
        /* Adjust text area for mobile */
        .stTextArea {
            min-height: 44px;
        }
        
        /* Adjust sidebar for mobile */
        section[data-testid="stSidebar"] {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Adjust expander for mobile */
        .streamlit-expanderHeader {
            min-height: 44px;
        }
    }
    
    /* Hide Streamlit branding for cleaner look */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Add some padding at the bottom for mobile */
    .main .block-container {
        padding-bottom: 80px;
    }
    
    /* Mobile navigation bar */
    .mobile-nav-bar {
        display: none;
    }
    
    @media (max-width: 768px) {
        .mobile-nav-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: white;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-around;
            padding: 10px 0;
            z-index: 1000;
        }
        
        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 0.7rem;
            color: #666;
            text-decoration: none;
        }
        
        .nav-icon {
            font-size: 1.5rem;
            margin-bottom: 4px;
        }
        
        .active {
            color: #2E86AB;
            font-weight: bold;
        }
    }
</style>
""", unsafe_allow_html=True)

# Add mobile detection
is_mobile = True  # Default to mobile-friendly layout for all devices
if 'is_mobile_checked' not in st.session_state:
    # This is a simple way to try to detect mobile devices
    # A more robust solution would use a proper user-agent parser
    user_agent = st.experimental_get_query_params().get('ua', [''])[0].lower()
    is_mobile_device = any(device in user_agent for device in ['mobile', 'android', 'iphone', 'ipad', 'ipod'])
    st.session_state.is_mobile_device = is_mobile_device
    st.session_state.is_mobile_checked = True
else:
    is_mobile_device = st.session_state.is_mobile_device

# Add mobile navigation bar to all pages
def add_mobile_navbar(current_page):
    if is_mobile:
        pages = ["Welcome", "Profile Setup", "Goals", "Affirmations", "Daily Reflection", "Dashboard"]
        icons = ["🏠", "👤", "🎯", "💭", "🌅", "📊"]
        
        nav_html = """
        <div class="mobile-nav-bar">
        """
        
        for i, page in enumerate(pages):
            active_class = "active" if page == current_page else ""
            nav_html += f"""
            <a href="javascript:void(0);" onclick="navigateToPage('{page}')" class="nav-item {active_class}">
                <div class="nav-icon">{icons[i]}</div>
                <div>{page.split(' ')[0]}</div>
            </a>
            """
        
        nav_html += """
        </div>
        
        <script>
        function navigateToPage(page) {
            // Update session state via query parameters
            const url = new URL(window.location.href);
            url.searchParams.set('page', page);
            window.location.href = url.toString();
        }
        </script>
        """
        
        st.markdown(nav_html, unsafe_allow_html=True)

# Data persistence functions
def load_user_data():
    """Load user data from session state or initialize empty data"""
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            'profile': {},
            'life_areas': {},
            'goals': {},
            'affirmations': {},
            'daily_reflections': {}
        }
    return st.session_state.user_data

def save_user_data(data):
    """Save user data to session state"""
    st.session_state.user_data = data

# Life areas from the PDF
LIFE_AREAS = [
    "Health & Fitness",
    "Home & Family", 
    "Life purpose & contribution",
    "Social life & relationships",
    "Career, work & education",
    "Money & finances"
]

# Common hobbies list
COMMON_HOBBIES = [
    "Reading", "Sports", "Music", "Travel", "Cooking", "Photography", 
    "Art", "Gaming", "Gardening", "Writing", "Dancing", "Hiking",
    "Yoga", "Learning languages", "Volunteering", "Technology"
]

def main():
    user_data = load_user_data()
    
    # Check for page parameter in URL (for mobile navigation)
    params = st.experimental_get_query_params()
    if 'page' in params and params['page'][0] in ["Welcome", "Profile Setup", "Goals", "Affirmations", "Daily Reflection", "Dashboard"]:
        st.session_state.page = params['page'][0]
        # Clear the parameter to avoid loops
        st.experimental_set_query_params()
    
    # Initialize page in session state if not present
    if 'page' not in st.session_state:
        st.session_state.page = "Welcome"
    
    # Sidebar navigation
    st.sidebar.title("🎯 Handy Navigation")
    
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["Welcome", "Profile Setup", "Goals", "Affirmations", "Daily Reflection", "Dashboard"],
        index=["Welcome", "Profile Setup", "Goals", "Affirmations", "Daily Reflection", "Dashboard"].index(st.session_state.page)
    )
    
    # Update session state when selection changes
    st.session_state.page = page
    
    # Add mobile detection message (only visible in development)
    if st.sidebar.checkbox("Show Debug Info", False):
        st.sidebar.info("📱 Mobile-friendly mode active")
        st.sidebar.write(f"Session state: {st.session_state}")
        
    # Set the initial sidebar state based on device
    if is_mobile_device:
        st.sidebar.markdown("""
        <style>
        /* Auto-collapse sidebar on mobile */
        @media (max-width: 768px) {
            section[data-testid="stSidebar"][aria-expanded="true"] {
                display: none !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)
    
    if page == "Welcome":
        welcome_page()
        add_mobile_navbar(page)
    elif page == "Profile Setup":
        profile_setup(user_data)
        add_mobile_navbar(page)
    elif page == "Goals":
        goals_page(user_data)
        add_mobile_navbar(page)
    elif page == "Affirmations":
        affirmations_page(user_data)
        add_mobile_navbar(page)
    elif page == "Daily Reflection":
        daily_reflection_page(user_data)
        add_mobile_navbar(page)
    elif page == "Dashboard":
        dashboard_page(user_data)
        add_mobile_navbar(page)

def welcome_page():
    """Welcome and introduction page"""
    st.markdown('<h1 class="main-header">Handy</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">The goals-tracking app that makes you think more than twice – your life in your hands.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://via.placeholder.com/400x300/2E86AB/FFFFFF?text=Handy+App", use_column_width=True)
    
    st.markdown("---")
    
    # Show condensed content on mobile
    if is_mobile:
        st.subheader("🎯 What problems are we solving?")
        st.markdown("""
        • **Clarity about life goals**
        • **Progress tracking**
        • **Motivation & Accountability**
        • **Self optimization**
        """)
    else:
        st.subheader("🎯 What problems are we solving?")
        problems = [
            "**Clarity about life goals** (Klarheit über Lebensziele)",
            "**Progress and routine tracking** (Tracking von Fortschritt und Routinen)", 
            "**Motivation & Accountability**",
            "**Reflection through affirmations** (Reflexion über Affirmationen)",
            "**Self management & Self optimization**",
            "**Visibility & transparency**"
        ]
        
        for problem in problems:
            st.markdown(f"• {problem}")
    
    st.markdown("---")
    
    st.subheader("👥 Perfect for:")
    st.markdown("""
    **Tech-savvy, professionally motivated adults (22-40 years)** who:
    - Want to pursue their goals clearly
    - Are ready to pay for personalized self-optimization tools
    - Seek AI-supported productivity apps
    - Value daily routines and personal development
    """)
    
    # Add mobile-friendly tip
    st.markdown("""
    <div style="background-color: #f3f4f6; padding: 10px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #2E86AB;">
        <p style="margin: 0;"><strong>💡 Pro Tip:</strong> Bookmark this app for easy access!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get Started button
    if st.button("🚀 Get Started"):
        st.session_state.page = "Profile Setup"
        st.experimental_rerun()

def profile_setup(user_data):
    """User profile setup page"""
    st.title("👤 Profile Setup")
    st.markdown("Let's get to know you better to personalize your experience.")
    
    # Job input
    st.subheader("What is your current job?")
    job = st.text_input("Enter your job title:", 
                       value=user_data['profile'].get('job', ''),
                       placeholder="e.g., Marketing Manager")
    
    # Hobbies selection
    st.subheader("What are your hobbies?")
    selected_hobbies = st.multiselect(
        "Select your hobbies:",
        COMMON_HOBBIES,
        default=user_data['profile'].get('hobbies', [])
    )
    
    # Custom hobby input
    custom_hobby = st.text_input("Add a custom hobby:")
    if custom_hobby and st.button("Add Custom Hobby"):
        if custom_hobby not in selected_hobbies:
            selected_hobbies.append(custom_hobby)
            st.success(f"Added '{custom_hobby}' to your hobbies!")
    
    # Life areas prioritization
    st.subheader("Order these life areas by importance to you")
    st.markdown("Drag and drop or use the interface below to prioritize:")
    
    if 'life_area_priority' not in user_data['profile']:
        user_data['profile']['life_area_priority'] = LIFE_AREAS.copy()
    
    prioritized_areas = []
    for i, area in enumerate(LIFE_AREAS):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{i+1}. {area}**")
        with col2:
            priority = st.selectbox(f"Priority", range(1, 7), 
                                  key=f"priority_{area}",
                                  index=i)
            prioritized_areas.append((priority, area))
    
    # Sort by priority
    prioritized_areas.sort(key=lambda x: x[0])
    sorted_areas = [area for _, area in prioritized_areas]
    
    # Save profile data
    if st.button("Save Profile"):
        user_data['profile'].update({
            'job': job,
            'hobbies': selected_hobbies,
            'life_area_priority': sorted_areas,
            'setup_completed': True
        })
        save_user_data(user_data)
        st.success("Profile saved successfully! 🎉")
        st.balloons()

def goals_page(user_data):
    """Goals management page"""
    st.title("🎯 Goals Management")
    
    if not user_data['profile'].get('setup_completed'):
        st.warning("Please complete your profile setup first!")
        return
    
    life_areas = user_data['profile'].get('life_area_priority', LIFE_AREAS)
    
    # Initialize goals structure
    if 'goals' not in user_data:
        user_data['goals'] = {}
    
    for area in life_areas:
        st.markdown(f'<div class="life-area-card">', unsafe_allow_html=True)
        st.subheader(f"📋 {area}")
        
        # Current situation description
        current_situation_key = f"{area}_current"
        current_situation = st.text_area(
            "Describe your current situation:",
            value=user_data['goals'].get(current_situation_key, ''),
            key=current_situation_key,
            height=100
        )
        user_data['goals'][current_situation_key] = current_situation
        
        # Goals for this area
        if area not in user_data['goals']:
            user_data['goals'][area] = []
        
        st.markdown("**Your Goals:**")
        
        # Display existing goals
        for i, goal in enumerate(user_data['goals'][area]):
            with st.expander(f"Goal {i+1}: {goal.get('title', 'Untitled')}"):
                goal_title = st.text_input(f"Goal Title:", value=goal.get('title', ''), key=f"goal_title_{area}_{i}")
                goal_why = st.text_area(f"Why is this important?", value=goal.get('why', ''), key=f"goal_why_{area}_{i}")
                goal_how = st.text_area(f"How will you achieve it?", value=goal.get('how', ''), key=f"goal_how_{area}_{i}")
                empowering_beliefs = st.text_area(f"Empowering beliefs:", value=goal.get('empowering_beliefs', ''), key=f"goal_emp_{area}_{i}")
                limiting_beliefs = st.text_area(f"Limiting beliefs:", value=goal.get('limiting_beliefs', ''), key=f"goal_lim_{area}_{i}")
                
                # Update goal
                user_data['goals'][area][i] = {
                    'title': goal_title,
                    'why': goal_why,
                    'how': goal_how,
                    'empowering_beliefs': empowering_beliefs,
                    'limiting_beliefs': limiting_beliefs
                }
                
                if st.button(f"Remove Goal {i+1}", key=f"remove_goal_{area}_{i}"):
                    user_data['goals'][area].pop(i)
                    st.experimental_rerun()
        
        # Add new goal
        if st.button(f"➕ Add Goal for {area}", key=f"add_goal_{area}"):
            new_goal = {
                'title': '',
                'why': '',
                'how': '',
                'empowering_beliefs': '',
                'limiting_beliefs': ''
            }
            user_data['goals'][area].append(new_goal)
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")
    
    # Save goals
    if st.button("💾 Save All Goals"):
        save_user_data(user_data)
        st.success("Goals saved successfully!")

def affirmations_page(user_data):
    """Affirmations management page"""
    st.title("💭 Affirmations")
    
    # Initialize affirmations
    if 'affirmations' not in user_data:
        user_data['affirmations'] = []
    
    st.markdown("Create positive affirmations to reinforce your goals and beliefs.")
    
    # Examples
    with st.expander("💡 Examples of good affirmations"):
        st.markdown("""
        • "I go to sleep before 11 PM every night"
        • "I do not smoke cigarettes"
        • "I drink 2 liters of water per day"
        • "I exercise for 30 minutes daily"
        • "I read for 20 minutes each morning"
        • "I practice gratitude every evening"
        """)
    
    # Display existing affirmations
    st.subheader("Your Affirmations")
    
    for i, affirmation in enumerate(user_data['affirmations']):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            updated_text = st.text_input(f"Affirmation {i+1}:", 
                                       value=affirmation.get('text', ''), 
                                       key=f"aff_text_{i}")
            user_data['affirmations'][i]['text'] = updated_text
        
        with col2:
            priority = st.selectbox("Priority", 
                                  range(1, len(user_data['affirmations']) + 1),
                                  index=affirmation.get('priority', 1) - 1,
                                  key=f"aff_priority_{i}")
            user_data['affirmations'][i]['priority'] = priority
        
        with col3:
            if st.button("🗑️", key=f"delete_aff_{i}", help="Delete affirmation"):
                user_data['affirmations'].pop(i)
                st.experimental_rerun()
    
    # Add new affirmation
    st.subheader("Add New Affirmation")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        new_affirmation_text = st.text_input("Enter your affirmation:", key="new_affirmation")
    
    with col2:
        if st.button("➕ Add"):
            if new_affirmation_text:
                new_affirmation = {
                    'text': new_affirmation_text,
                    'priority': len(user_data['affirmations']) + 1,
                    'created_date': str(date.today())
                }
                user_data['affirmations'].append(new_affirmation)
                st.experimental_rerun()
    
    # AI Generation (placeholder)
    if st.button("🤖 Generate AI Affirmations"):
        st.info("AI generation would analyze your goals and beliefs to create personalized affirmations. This feature would be implemented with an AI service.")
        
        # Sample generated affirmations based on common goals
        sample_affirmations = [
            "I am committed to my health and make conscious choices daily",
            "I prioritize my relationships and invest time in meaningful connections", 
            "I am focused on my career growth and take action towards my professional goals",
            "I manage my finances wisely and build towards financial security"
        ]
        
        st.markdown("**Sample AI-generated affirmations:**")
        for sample in sample_affirmations:
            if st.button(f"➕ Add: {sample}", key=f"sample_{sample[:20]}"):
                new_affirmation = {
                    'text': sample,
                    'priority': len(user_data['affirmations']) + 1,
                    'created_date': str(date.today())
                }
                user_data['affirmations'].append(new_affirmation)
                st.experimental_rerun()
    
    # Save affirmations
    if st.button("💾 Save Affirmations"):
        save_user_data(user_data)
        st.success("Affirmations saved successfully!")

def daily_reflection_page(user_data):
    """Daily reflection and affirmation rating page"""
    st.title("🌅 Daily Reflection")
    
    today = str(date.today())
    
    # Initialize daily reflections
    if 'daily_reflections' not in user_data:
        user_data['daily_reflections'] = {}
    
    if today not in user_data['daily_reflections']:
        user_data['daily_reflections'][today] = {}
    
    st.markdown(f"**Reflection for {datetime.now().strftime('%B %d, %Y')}**")
    
    if not user_data.get('affirmations'):
        st.warning("You haven't created any affirmations yet. Please visit the Affirmations page first.")
        return
    
    st.markdown("Rate each affirmation based on how well you followed it today:")
    st.markdown("• **0-10**: How well did you follow this affirmation?")
    st.markdown("• **X**: Mark as not relevant for today")
    
    # Sort affirmations by priority
    sorted_affirmations = sorted(user_data['affirmations'], key=lambda x: x.get('priority', 999))
    
    for i, affirmation in enumerate(sorted_affirmations):
        st.markdown(f'<div class="affirmation-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"**{affirmation['text']}**")
        
        with col2:
            # Rating slider
            rating = st.slider(
                "Rating", 
                min_value=0, 
                max_value=10, 
                value=user_data['daily_reflections'][today].get(f"aff_{i}_rating", 5),
                key=f"rating_{i}_{today}"
            )
            user_data['daily_reflections'][today][f"aff_{i}_rating"] = rating
        
        with col3:
            # Not relevant checkbox
            not_relevant = st.checkbox(
                "Not relevant (X)", 
                value=user_data['daily_reflections'][today].get(f"aff_{i}_not_relevant", False),
                key=f"not_relevant_{i}_{today}"
            )
            user_data['daily_reflections'][today][f"aff_{i}_not_relevant"] = not_relevant
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional reflection notes
    st.subheader("📝 Additional Notes")
    reflection_notes = st.text_area(
        "How was your day? Any insights or thoughts?",
        value=user_data['daily_reflections'][today].get('notes', ''),
        height=100
    )
    user_data['daily_reflections'][today]['notes'] = reflection_notes
    
    # Mood tracking
    st.subheader("😊 Mood")
    mood_options = ["😢 Very Low", "😕 Low", "😐 Neutral", "🙂 Good", "😊 Very Good"]
    mood = st.selectbox(
        "How was your overall mood today?",
        mood_options,
        index=user_data['daily_reflections'][today].get('mood_index', 2)
    )
    user_data['daily_reflections'][today]['mood'] = mood
    user_data['daily_reflections'][today]['mood_index'] = mood_options.index(mood)
    
    # Save reflection
    if st.button("💾 Save Today's Reflection"):
        user_data['daily_reflections'][today]['completed'] = True
        user_data['daily_reflections'][today]['completion_time'] = datetime.now().isoformat()
        save_user_data(user_data)
        st.success("Daily reflection saved! 🌟")
        st.balloons()

def dashboard_page(user_data):
    """Dashboard with overview and analytics"""
    st.title("📊 Dashboard")
    
    if not user_data['profile'].get('setup_completed'):
        st.warning("Please complete your profile setup first!")
        return
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_goals = sum(len(goals) for goals in user_data.get('goals', {}).values() if isinstance(goals, list))
    total_affirmations = len(user_data.get('affirmations', []))
    reflection_days = len(user_data.get('daily_reflections', {}))
    
    with col1:
        st.metric("🎯 Total Goals", total_goals)
    
    with col2:
        st.metric("💭 Affirmations", total_affirmations)
    
    with col3:
        st.metric("📅 Reflection Days", reflection_days)
    
    with col4:
        completion_rate = 0
        if user_data.get('daily_reflections'):
            completed_days = sum(1 for day_data in user_data['daily_reflections'].values() 
                               if day_data.get('completed'))
            completion_rate = (completed_days / len(user_data['daily_reflections'])) * 100
        st.metric("✅ Completion Rate", f"{completion_rate:.0f}%")
    
    st.markdown("---")
    
    # Goals by life area
    st.subheader("🎯 Goals by Life Area")
    if user_data.get('goals'):
        goal_counts = {}
        for area, goals in user_data['goals'].items():
            if isinstance(goals, list) and goals:
                goal_counts[area] = len(goals)
        
        if goal_counts:
            goal_df = pd.DataFrame(list(goal_counts.items()), columns=['Life Area', 'Goal Count'])
            st.bar_chart(goal_df.set_index('Life Area'))
    
    # Recent reflections
    st.subheader("📈 Recent Mood Trends")
    if user_data.get('daily_reflections'):
        mood_data = []
        for date_str, reflection in user_data['daily_reflections'].items():
            if 'mood_index' in reflection:
                mood_data.append({
                    'Date': pd.to_datetime(date_str),
                    'Mood': reflection['mood_index']
                })
        
        if mood_data:
            mood_df = pd.DataFrame(mood_data).sort_values('Date')
            st.line_chart(mood_df.set_index('Date'))
    
    # Profile summary
    st.subheader("👤 Profile Summary")
    profile = user_data.get('profile', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Job:** {profile.get('job', 'Not specified')}")
        if profile.get('hobbies'):
            st.markdown(f"**Hobbies:** {', '.join(profile['hobbies'])}")
    
    with col2:
        if profile.get('life_area_priority'):
            st.markdown("**Life Area Priorities:**")
            for i, area in enumerate(profile['life_area_priority'][:3], 1):
                st.markdown(f"{i}. {area}")
    
    # Export data
    st.subheader("💾 Data Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Data"):
            # Create downloadable JSON
            export_data = json.dumps(user_data, indent=2, default=str)
            st.download_button(
                label="Download JSON",
                data=export_data,
                file_name=f"handy_data_{date.today()}.json",
                mime="application/json"
            )
    
    with col2:
        uploaded_file = st.file_uploader("📤 Import Data", type="json")
        if uploaded_file is not None:
            try:
                imported_data = json.load(uploaded_file)
                if st.button("Confirm Import"):
                    st.session_state.user_data = imported_data
                    st.success("Data imported successfully!")
                    st.experimental_rerun()
            except json.JSONDecodeError:
                st.error("Invalid JSON file")

if __name__ == "__main__":
    main()