import streamlit as st
 
st.title('Departments')
 
# Create tabs
tab_titles = ['Definitions', 'Part-ARO', 'Part-ORO','Part-CAT', 'Part-NCC', 'Part-NCO','Part-SPA','Part-SPO' ]
tabs = st.tabs(tab_titles)
 
# Add content to each tab
with tabs[0]:
    st.header('Definitions')
    for ticket in st.session_state['Definitions']:
        st.write(str(st.session_state['Definitions'].index(ticket)+1)+" : "+ticket)
    
with tabs[1]:
    st.header('Part-ARO')
    for ticket in st.session_state['Part-ARO']:
        st.write(str(st.session_state['Part-ARO'].index(ticket)+1)+" : "+ticket)

with tabs[2]:
    st.header('Part-ORO')
    for ticket in st.session_state['Part-ORO']:
        st.write(str(st.session_state['Part-ORO'].index(ticket)+1)+" : "+ticket)

with tabs[3]:
    st.header('Part-CAT')
    for ticket in st.session_state['Part-CAT']:
        st.write(str(st.session_state['Part-CAT'].index(ticket)+1)+" : "+ticket)

with tabs[4]:
    st.header('Part-NCC')
    for ticket in st.session_state['Part-NCC']:
        st.write(str(st.session_state['Part-NCC'].index(ticket)+1)+" : "+ticket)

with tabs[5]:
    st.header('Part-NCO')
    for ticket in st.session_state['Part-NCO']:
        st.write(str(st.session_state['Part-NCO'].index(ticket)+1)+" : "+ticket)

with tabs[6]:
    st.header('Part-SPO')
    for ticket in st.session_state['Part-SPO']:
        st.write(str(st.session_state['Part-SPO'].index(ticket)+1)+" : "+ticket)

with tabs[7]:
    st.header('Part-SPA')
    for ticket in st.session_state['Part-SPA']:
        st.write(str(st.session_state['Part-SPA'].index(ticket)+1)+" : "+ticket)




    
 