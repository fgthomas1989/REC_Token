import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe

st.set_page_config(layout="centered", page_icon="🎓", page_title="REC Generator")
st.title("REC PDF Generator")

st.write(
    "Claiming this token will generate a Renewable Energy Certificate (REC) and will grant you it's attributes."
)

left, right = st.columns(5)

right.write("Here is what your REC will look like:")

right.image("template.png", width=300)

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("template.html")


left.write("Fill in the data:")
form = left.form("template_form")
renewable_facility_location = form.text_input("Renewable Facility Location")
fuel = form.selectbox(
    "Choose fuel",
    ["Wind", "Solar"],
    index=0,
)
total_energy = form.slider("MWh", 1, 100, 60)
submit = form.form_submit_button("Generate PDF")

if submit:
    html = template.render(
        fuel=fuel,
        fuel=fuel,
        total_energy=f"{total_energy}/100",
        date=date.today().strftime("%B %d, %Y"),
    )

    pdf = pdfkit.from_string(html, False)
    st.balloons()

    right.success("Your REC was generated!")
    # st.write(html, unsafe_allow_html=True)
    # st.write("")
    right.download_button(
        "⬇️ Download PDF",
        data=pdf,
        file_name="REC.pdf",
        mime="application/octet-stream",
    )
