# ui/pages/dashboard.py
import streamlit as st
from datetime import datetime
from typing import Optional
from models.project import Project, ProjectStatus, ProjectPriority, ProjectMilestone
from database.project_store import ProjectStore
import uuid

class DashboardPage:
    def __init__(self):
        self.project_store = ProjectStore()

    def render(self) -> None:
        st.title("Company Portfolio Dashboard")
        
        # Sidebar filters
        with st.sidebar:
            st.subheader("Filters")
            status_filter = st.multiselect(
                "Status",
                options=[status.value for status in ProjectStatus],
                default=[]
            )
            priority_filter = st.multiselect(
                "Priority",
                options=[priority.value for priority in ProjectPriority],
                default=[]
            )

        # Main content
        tabs = st.tabs(["Projects Overview", "Project Details", "Analytics"])
        
        with tabs[0]:
            self._render_projects_overview(status_filter, priority_filter)
        
        with tabs[1]:
            self._render_project_details()
            
        with tabs[2]:
            self._render_analytics()

    def _render_projects_overview(self, status_filter: list, priority_filter: list) -> None:
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("➕ New Project", type="primary"):
                st.session_state["show_project_form"] = True

        projects = self.project_store.get_all_projects()
        
        # Apply filters
        if status_filter:
            projects = [p for p in projects if p.status.value in status_filter]
        if priority_filter:
            projects = [p for p in projects if p.priority.value in priority_filter]

        # Project cards
        for project in projects:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.subheader(project.name)
                    st.text(f"Status: {project.status.value}")
                    
                with col2:
                    st.progress(project.progress, text=f"Progress: {project.progress}%")
                    st.text(f"Budget: ${project.spent:,.2f} / ${project.budget:,.2f}")
                    
                with col3:
                    st.text(f"Priority: {project.priority.value}")
                    if st.button("Details", key=f"detail_{project.id}"):
                        st.session_state["selected_project"] = project.id

    def _render_project_details(self) -> None:
        if "selected_project" in st.session_state:
            project = self.project_store.get_project(st.session_state["selected_project"])
            if project:
                self._render_project_form(project)
        elif st.session_state.get("show_project_form", False):
            self._render_project_form()

    def _render_project_form(self, project: Optional[Project] = None) -> None:
        is_edit = project is not None
        form_key = "edit_project" if is_edit else "new_project"
        
        with st.form(key=form_key):
            name = st.text_input("Project Name", value=project.name if is_edit else "")
            description = st.text_area("Description", value=project.description if is_edit else "")
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(
                    "Start Date",
                    value=project.start_date.date() if is_edit else datetime.now().date()
                )
                status = st.selectbox(
                    "Status",
                    options=[s.value for s in ProjectStatus],
                    index=[s.value for s in ProjectStatus].index(project.status.value) if is_edit else 0
                )
                budget = st.number_input(
                    "Budget ($)",
                    value=project.budget if is_edit else 0.0,
                    min_value=0.0
                )
                
            with col2:
                end_date = st.date_input(
                    "End Date",
                    value=project.end_date.date() if is_edit else datetime.now().date()
                )
                priority = st.selectbox(
                    "Priority",
                    options=[p.value for p in ProjectPriority],
                    index=[p.value for p in ProjectPriority].index(project.priority.value) if is_edit else 0
                )
                progress = st.slider(
                    "Progress (%)",
                    value=float(project.progress) if is_edit else 0.0,
                    min_value=0.0,
                    max_value=100.0
                )

            # Team members
            st.subheader("Team Members")
            team_members = st.multiselect(
                "Select team members",
                options=self._get_available_team_members(),
                default=project.team_members if is_edit else []
            )

            submitted = st.form_submit_button("Save Project")
            if submitted:
                try:
                    new_project = Project(
                        id=project.id if is_edit else str(uuid.uuid4()),
                        name=name,
                        description=description,
                        start_date=datetime.combine(start_date, datetime.min.time()),
                        end_date=datetime.combine(end_date, datetime.min.time()),
                        status=ProjectStatus(status),
                        priority=ProjectPriority(priority),
                        budget=budget,
                        progress=progress,
                        team_members=team_members,
                        spent=project.spent if is_edit else 0.0,
                        created_at=project.created_at if is_edit else datetime.now()
                    )
                    
                    if is_edit:
                        success = self.project_store.update_project(new_project)
                        if success:
                            st.success("Project updated successfully!")
                        else:
                            st.error("Failed to update project")
                    else:
                        success = self.project_store.create_project(new_project)
                        if success:
                            st.success("Project created successfully!")
                            st.session_state["show_project_form"] = False
                        else:
                            st.error("Failed to create project")
                            
                except Exception as e:
                    st.error(f"Error saving project: {str(e)}")

    def _render_analytics(self) -> None:
        projects = self.project_store.get_all_projects()
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Projects", len(projects))
        
        with col2:
            active_projects = len([p for p in projects if p.status == ProjectStatus.IN_PROGRESS])
            st.metric("Active Projects", active_projects)
        
        with col3:
            total_budget = sum(p.budget for p in projects)
            st.metric("Total Budget", f"${total_budget:,.2f}")
        
        with col4:
            total_spent = sum(p.spent for p in projects)
            st.metric("Total Spent", f"${total_spent:,.2f}")