import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
breed = st.text_input("Breed", value="Unknown")
age = st.number_input("Age", min_value=0.0, value=1.0)
gender = st.selectbox("Gender", ["Male", "Female", "Unknown"])

if st.button("Create Owner and Pet"):
    owner = Owner(owner_name)
    pet = Pet(pet_name, species, breed, age, gender)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.pet = pet
    st.success(f"Owner '{owner_name}' and pet '{pet_name}' created!")

st.markdown("### Tasks")
st.caption("Add tasks for the pet. These will create Task objects and add them to the pet.")

if "pet" in st.session_state:
    pet = st.session_state.pet
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_type = st.selectbox("Task type", ["feeding", "vet", "grooming", "medication", "walks"])
    with col2:
        task_title = st.text_input("Task title/notes", value="Morning walk")
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        from datetime import datetime
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        task = Task(
            task_type=task_type,
            pet=pet,
            date=current_date,
            notes=task_title,
            duration=duration,
            priority=priority
        )
        pet.tasks.append(task)
        st.success(f"Task '{task_title}' added to {pet.name}!")

    if pet.tasks:
        st.write("Current tasks for pet:")
        for task in pet.tasks:
            st.write(task.get_summary())
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Create an owner and pet first.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate and display the schedule for the pet.")

if st.button("Generate schedule"):
    if "pet" in st.session_state:
        pet = st.session_state.pet
        st.write("### Scheduled Tasks:")
        for task in pet.tasks:
            st.write(f"- {task.get_summary()}")
        if not pet.tasks:
            st.info("No tasks to schedule. Add some tasks first.")
    else:
        st.warning("Create an owner and pet first.")

