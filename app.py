import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

ROOT=Path(__file__).parent
ASSETS=ROOT/"assets"
def asset_file(filename):
    """Find an asset in assets/ first, then at repository root (GitHub browser uploads)."""
    for candidate in (ASSETS/filename, ROOT/filename):
        if candidate.exists():
            return candidate
    return None
LOGO=asset_file("frostwise_logo.png")
FACILITY=asset_file("refrigeration_facility_ai_visual.png")
PRODUCTS=[
    ("Vegetable Cold Storage","vegetable_cold_storage.jpg"),("Meat Processing Cold Room","meat_processing_cold_room.jpg"),
    ("Dairy Processing Unit","dairy_processing_unit.jpg"),("Seafood Cold Storage","seafood_cold_storage.jpg"),
    ("Supermarket Display Chiller","supermarket_display_chiller.jpg"),("Pharma Cold Storage","pharma_cold_storage.jpg"),
    ("Fruit Cold Storage","fruit_cold_storage.jpg"),("Refrigerated Transport","refrigerated_transport.jpg"),
    ("Hotel & Restaurant Cooling","hotel_restaurant_cold_room.jpg"),("Industrial Chiller System","industrial_chiller_system.jpg")
]
TEAM=[("Sudhirsun S","Team Member"),("Zain Abbas A","Team Member"),("Sundar H","Team Member"),("Subramanian M","Team Member")]
REQUIRED=["timestamp","room_temperature_c","setpoint_c","ambient_temperature_c","compressor_power_kw"]
st.set_page_config(page_title="FROSTWISE | Smart Refrigeration",page_icon="❄️",layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--navy:#102a43;--blue:#1597d4;--teal:#13b8a6;--green:#55c878;--ink:#142b3b;--muted:#627789;--line:#dce8ef}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;color:var(--ink)}
.stApp{background:linear-gradient(180deg,#f7fbfd 0%,#fff 50%,#f8fbfd 100%)}
.block-container{max-width:1380px;padding-top:1rem;padding-bottom:2.4rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#edf7fb,#f8fbfd);border-right:1px solid var(--line)}
.hero{padding:2.15rem;border-radius:23px;background:linear-gradient(118deg,#102a43,#174d70 56%,#087f8c);color:#fff;box-shadow:0 16px 40px #102a4318;margin:.8rem 0 1.2rem}
.eyebrow{text-transform:uppercase;letter-spacing:.16em;font-size:.72rem;font-weight:800;color:#8ce6e0;margin-bottom:.7rem}
.hero h1{font-family:Manrope,sans-serif;color:#fff;font-size:2.7rem;line-height:1.08;font-weight:800;letter-spacing:-.04em;margin:0}
.hero p{color:#dceef5;font-size:1.04rem;max-width:760px;margin:.8rem 0 0}
.hero-foot{color:#bfe6ef;font-size:.76rem;font-weight:700;letter-spacing:.1em;margin-top:1.1rem}
.kicker{text-transform:uppercase;letter-spacing:.15em;color:#168ba8;font-size:.7rem;font-weight:800;margin:.65rem 0 .25rem}
.heading{font-family:Manrope,sans-serif;font-size:1.55rem;font-weight:800;color:#102a43;letter-spacing:-.03em;margin:0 0 .25rem}
.sub{color:#698091;font-size:.92rem;margin-bottom:1rem}
.card{background:#fff;border:1px solid #dce8ef;border-radius:17px;padding:1.1rem;box-shadow:0 6px 22px #102a4308;height:100%;margin-bottom:.7rem}
.card h3{color:#102a43;font-family:Manrope,sans-serif;font-size:1.05rem;margin:.2rem 0 .5rem}
.card p{color:#627789;font-size:.9rem;line-height:1.55}
.tag{display:inline-block;background:#e5f7f4;color:#087f76;border:1px solid #c4eee6;border-radius:99px;padding:.28rem .65rem;font-size:.7rem;font-weight:800;letter-spacing:.04em}
[data-testid="stMetric"]{background:#fff;border:1px solid var(--line);border-radius:15px;padding:1rem;box-shadow:0 5px 18px #102a4308}
[data-testid="stMetricValue"]{font-family:Manrope,sans-serif;color:#102a43;font-weight:800}
.stButton>button,.stDownloadButton>button{border-radius:10px;font-weight:700;border:1px solid #c9dce7}
.stButton>button[kind="primary"]{background:linear-gradient(90deg,#087f8c,#1597d4);border:0}
div[data-testid="stForm"]{background:#fff;border:1px solid var(--line);padding:1.1rem;border-radius:16px}
.footer{border-top:1px solid var(--line);margin-top:2.5rem;padding-top:1rem;color:#718595;font-size:.78rem}
@media(max-width:760px){.hero{padding:1.35rem}.hero h1{font-size:2rem}}
</style>""",unsafe_allow_html=True)

def hero(k,t,s,foot="MONITOR  ·  ANALYZE  ·  DETECT  ·  OPTIMIZE"):
    st.markdown(f'<div class="hero"><div class="eyebrow">{k}</div><h1>{t}</h1><p>{s}</p><div class="hero-foot">{foot}</div></div>',unsafe_allow_html=True)
def section(k,t,s=""):
    st.markdown(f'<div class="kicker">{k}</div><div class="heading">{t}</div><div class="sub">{s}</div>',unsafe_allow_html=True)
def demo_data():
    rng=np.random.default_rng(7); n=72
    ts=pd.date_range(end=pd.Timestamp.now().floor("h"),periods=n,freq="h")
    amb=29+4*np.sin(np.arange(n)*2*np.pi/24)+rng.normal(0,.8,n)
    room=-18+rng.normal(0,.45,n); power=8.5+.10*(amb-29)+rng.normal(0,.35,n)
    room[35:39]+=np.array([2,3,3.4,2.2]); power[48:53]+=3.2
    return pd.DataFrame({"timestamp":ts,"room_temperature_c":np.round(room,2),"setpoint_c":-18.0,"ambient_temperature_c":np.round(amb,2),"compressor_power_kw":np.round(np.maximum(power,.1),2)})

with st.sidebar:
    if LOGO: st.image(str(LOGO),use_container_width=True)
    st.markdown("### FROSTWISE")
    st.caption("Smart refrigeration intelligence")
    st.markdown('<span class="tag">PROTOTYPE ENVIRONMENT</span>',unsafe_allow_html=True)
    st.divider()
    st.caption("Navigate using the menu across the top of the website.")
    st.markdown("**Contact**")
    st.caption("The contact form prepares a draft locally; it does not send email automatically.")

st.markdown('<span class="tag">SMART REFRIGERATION INTELLIGENCE</span> &nbsp; <span style="color:#6a8291;font-size:.82rem">Prototype environment · v1.0</span>',unsafe_allow_html=True)
# Brand header
brand_left, brand_right = st.columns([1, 4])
with brand_left:
    if LOGO: st.image(str(LOGO), width=220)
with brand_right:
    st.markdown("<div style='padding-top:22px;text-align:right;color:#1597d4;font-weight:800;letter-spacing:.12em'>SMART REFRIGERATION SOLUTIONS</div>",unsafe_allow_html=True)
page=st.radio("Website navigation",["Home","Our Solution","Products & Applications","Our Team","Who Benefits","Ask FROSTWISE","Contact","Live Dashboard"],horizontal=True,label_visibility="collapsed")
st.divider()

if page=="Home":
    left,right=st.columns([1.05,.95],gap="large")
    with left:
        hero("Commercial refrigeration · AI-assisted monitoring","Make every cooling hour count.","FROSTWISE turns refrigeration operating data into clearer energy insights, early anomaly signals and practical next steps for the people who keep cold-chain systems running.")
        st.markdown('<span class="tag">ENERGY VISIBILITY</span> &nbsp; <span class="tag">EARLY SIGNALS</span> &nbsp; <span class="tag">ACTIONABLE INSIGHTS</span>',unsafe_allow_html=True)
        st.write("Built for teams that need to understand temperature stability, compressor behaviour and energy trends in one place.")
    with right:
        if FACILITY: st.image(str(FACILITY),use_container_width=True,caption="AI-generated concept image · illustrative, not a customer installation")
        st.markdown('<div class="card"><h3>Designed for better decisions</h3><p>See temperature drift, unusual compressor power and energy trends in one workspace—then investigate with clearer context.</p></div>',unsafe_allow_html=True)
    section("Our team","The people behind FROSTWISE","A team working together on smarter, more efficient refrigeration insights.")
    team_cols=st.columns(4)
    for col,(member,role) in zip(team_cols,TEAM):
        with col:
            initials="".join(part[0] for part in member.split()[:2]).upper()
            st.markdown(f"<div class='card' style='text-align:center'><div style='width:76px;height:76px;border-radius:50%;margin:0 auto 12px;background:linear-gradient(135deg,#dff5ff,#d9f6e6);display:flex;align-items:center;justify-content:center;color:#075985;font-size:1.45rem;font-weight:800;border:3px solid white;box-shadow:0 0 0 1px #cde5f2'>{initials}</div><h3>{member}</h3><p>{role}</p></div>",unsafe_allow_html=True)
    section("Products in customer environments","Refrigeration applications across industries","AI-generated illustrative concept images—not photographs of confirmed customer installations.")
    product_cols=st.columns(5)
    for col,(title,filename) in zip(product_cols,PRODUCTS[:5]):
        with col:
            img=asset_file(filename)
            if img: st.image(str(img),use_container_width=True)
            st.caption(title)
    if st.button("Explore all product applications",type="primary"):
        st.session_state["show_product_gallery"]=True
    if st.session_state.get("show_product_gallery"):
        product_cols=st.columns(5)
        for col,(title,filename) in zip(product_cols,PRODUCTS[5:]):
            with col:
                img=asset_file(filename)
                if img: st.image(str(img),use_container_width=True)
                st.caption(title)
    section("Platform overview","From operating data to next steps","A simple workflow for teams managing commercial cooling equipment.")
    cols=st.columns(3)
    for col,(n,t,d) in zip(cols,[("01","Monitor","Bring temperature, setpoint, ambient conditions and compressor power into one view."),("02","Detect","Flag persistent temperature deviations and unusual power readings for investigation."),("03","Optimize","Explore energy trends and illustrative savings scenarios to prioritize follow-up.")]):
        with col: st.markdown(f'<div class="card"><span class="tag">{n}</span><h3>{t}</h3><p>{d}</p></div>',unsafe_allow_html=True)
    section("Our approach","Useful signals, clear limitations","This prototype uses sample data and configurable screening rules. Real deployment requires site data, validation and customer feedback.")
    st.info("FROSTWISE supports investigation. It does not control equipment or replace qualified refrigeration technicians.")

elif page=="Our Solution":
    hero("Our solution","Refrigeration insights, made actionable.","Analyze commercial refrigeration readings, identify patterns worth checking and communicate suggested next steps.")
    if FACILITY: st.image(str(FACILITY),use_container_width=True,caption="AI-generated illustrative refrigeration facility")
    section("How it works","A clear analysis workflow","Upload structured readings or explore the built-in demo dataset.")
    cols=st.columns(3)
    for col,(t,d) in zip(cols,[("1. Ingest data","Read timestamped room temperature, setpoint, ambient temperature and compressor power from CSV."),("2. Analyze patterns","Calculate energy estimates, temperature deviations and a data-derived power screening threshold."),("3. Explain signals","Show evidence and inspection prompts so an operator can decide what to check next.")]):
        with col: st.markdown(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>',unsafe_allow_html=True)
    section("Current capabilities","Available in the prototype")
    a,b=st.columns(2)
    with a:
        st.markdown('<div class="card"><h3>Energy visibility</h3><p>Estimated kWh, indicative cost, compressor power profile, daily trends and adjustable savings scenarios.</p></div><div class="card"><h3>Temperature screening</h3><p>Flag sustained deviations from the configured setpoint threshold.</p></div>',unsafe_allow_html=True)
    with b:
        st.markdown('<div class="card"><h3>CSV data upload</h3><p>Analyze readings with required columns and export resulting data and signal logs.</p></div><div class="card"><h3>Power anomaly screening</h3><p>Flag unusual compressor power relative to the selected dataset. Signals are not confirmed diagnoses.</p></div>',unsafe_allow_html=True)
    st.warning("The current engine uses explicit rules and robust statistics, not a trained AI model. Alerts do not prove a fault or identify root cause.")

elif page=="Products & Applications":
    hero("Products & applications","Cooling solutions across customer environments.","Explore illustrative refrigeration environments where monitoring and energy insights may be useful.")
    st.info("All gallery images are AI-generated concept visuals for demonstration. They do not represent verified customers, deployments or installed FROSTWISE products.")
    for start in range(0,len(PRODUCTS),5):
        cols=st.columns(5)
        for col,(title,filename) in zip(cols,PRODUCTS[start:start+5]):
            with col:
                img=asset_file(filename)
                if img: st.image(str(img),use_container_width=True)
                st.markdown(f"<div class='card'><h3>{title}</h3><p>Illustrative application for refrigeration monitoring and energy visibility.</p></div>",unsafe_allow_html=True)

elif page=="Our Team":
    hero("Meet the team","The people behind FROSTWISE.","A collaborative team exploring smarter refrigeration, monitoring and energy insights.")
    team_cols=st.columns(4)
    team_details=[("Sudhirsun S","Team Member","Project coordination and solution planning"),("Zain Abbas A","Team Member","Research and data analysis"),("Sundar H","Team Member","Product development and AI integration"),("Subramanian M","Team Member","Testing and implementation")]
    for col,(member,role,description) in zip(team_cols,team_details):
        with col:
            initials="".join(part[0] for part in member.split()[:2]).upper()
            st.markdown(f"<div class='card' style='text-align:center'><div style='width:94px;height:94px;border-radius:50%;margin:0 auto 14px;background:linear-gradient(135deg,#dff5ff,#d9f6e6);display:flex;align-items:center;justify-content:center;color:#075985;font-size:1.7rem;font-weight:800;border:3px solid white;box-shadow:0 0 0 1px #cde5f2'>{initials}</div><h3>{member}</h3><p><b>{role}</b><br>{description}</p></div>",unsafe_allow_html=True)
    section("Our mission","Make refrigeration smarter and more sustainable","We are building a prototype that makes refrigeration operating data easier to review, discuss and improve.")
    st.caption("Team roles are editable descriptions for the website. Please confirm each role with your team before presenting them as official.")

elif page=="Who Benefits":
    hero("Who benefits","One cold chain. Many people to support.","Designed for teams that rely on stable temperatures, efficient cooling and dependable equipment.")
    audience=[
    ("Supermarkets & grocery","Review display-case and cold-room operating patterns, investigate excursions and create a consistent escalation record."),
    ("Restaurants & food service","Investigate walk-in cooler and freezer behaviour, with clearer signals for follow-up."),
    ("Food processing & cold storage","Review power patterns, temperature stability and operating history across datasets."),
    ("Refrigeration service providers","Use signal logs as a starting point for site inspections and customer conversations."),
    ("Facility & energy managers","Connect operating conditions with estimated energy use and costs to prioritize follow-up."),
    ("Equipment owners & operators","Make refrigeration data easier to understand and share in operational discussions.")]
    cols=st.columns(3)
    for i,(t,d) in enumerate(audience):
        with cols[i%3]: st.markdown(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>',unsafe_allow_html=True)
    st.info("These are intended user groups, not confirmed customers. Benefits must be validated through interviews and pilot testing.")

elif page=="Ask FROSTWISE":
    hero("FROSTWISE assistant","Ask a refrigeration or prototype question.","Ask about the demo, energy estimates, alert logic, CSV upload and suggested inspection checks.")
    if "chat_history" not in st.session_state: st.session_state.chat_history=[]
    faq=[
    (["what is frostwise","what does this do","purpose","about"],"FROSTWISE is a prototype that analyzes commercial refrigeration readings, estimates energy and cost, and flags unusual temperature or compressor-power patterns for investigation."),
    (["energy","kwh","electricity cost","tariff","bill"],"The prototype estimates energy by treating each row as one hour of average compressor power. Estimated cost = estimated kWh × the tariff you set. If your data uses another sampling interval, the calculation must be adjusted."),
    (["temperature","setpoint","temperature alert","excursion"],"A temperature signal is raised when the absolute difference between room temperature and setpoint meets the configured limit for consecutive readings. Check sensor accuracy, door openings, product loading and system operation."),
    (["compressor","power anomaly","unusual power","threshold"],"The prototype flags compressor-power readings above a robust threshold derived from the selected dataset. Compare cooling demand, ambient conditions, operating logs and condenser condition. This is only a screening signal."),
    (["ai","artificial intelligence","machine learning"],"The current version uses explicit rules and robust statistics, not a trained AI model or live AI API. The next step is to validate the logic against real refrigeration data and expert-labelled events."),
    (["csv","upload","columns","data format"],"CSV upload requires these exact columns: timestamp, room_temperature_c, setpoint_c, ambient_temperature_c, compressor_power_kw."),
    (["fault","diagnosis","broken","failure"],"FROSTWISE does not confirm a fault or root cause. It flags readings for investigation. Follow site safety procedures and have a qualified refrigeration technician verify equipment conditions.")]
    for role,msg in st.session_state.chat_history:
        with st.chat_message(role): st.markdown(msg)
    prompt=st.chat_input("Ask about energy, alerts, CSV upload, or the prototype…")
    if prompt:
        st.session_state.chat_history.append(("user",prompt)); p=prompt.lower(); ans=None
        for keys,reply in faq:
            if any(k in p for k in keys): ans=reply; break
        if ans is None: ans="I can help with the current prototype, energy calculations, temperature alerts, compressor-power screening and CSV format. This assistant uses a local FAQ knowledge base, not a live generative AI service. For equipment diagnosis, consult a qualified refrigeration technician."
        st.session_state.chat_history.append(("assistant",ans)); st.rerun()
    st.caption("Prototype disclosure: local FAQ assistant, not a live AI model. Do not enter confidential facility data.")
    if st.button("Clear conversation"): st.session_state.chat_history=[]; st.rerun()

elif page=="Contact":
    hero("Contact FROSTWISE","Let's explore a smarter cold chain.","Share a question, pilot interest or feedback. This demo form prepares a message locally and does not send email automatically.")
    left,right=st.columns([1,1],gap="large")
    with left:
        section("Get in touch","Tell us what you need")
        with st.form("contact_form"):
            name=st.text_input("Name"); org=st.text_input("Organization (optional)"); email=st.text_input("Email address")
            topic=st.selectbox("Reason for contacting",["Prototype feedback","Pilot discussion","Technical question","Partnership enquiry","Other"])
            message=st.text_area("Message",height=130,placeholder="Tell us about your refrigeration use case or question…")
            submit=st.form_submit_button("Prepare enquiry",type="primary")
        if submit:
            if not name.strip() or not email.strip() or not message.strip(): st.error("Please enter your name, email and message.")
            else:
                st.session_state["contact_draft"]=f"Subject: {topic}\nName: {name}\nOrganization: {org or 'Not provided'}\nReply email: {email}\n\n{message}"
                st.success("Enquiry draft prepared. Copy it into your email client to send.")
        if st.session_state.get("contact_draft"):
            st.text_area("Enquiry draft",st.session_state["contact_draft"],height=170)
            st.download_button("Download enquiry TXT",st.session_state["contact_draft"],"frostwise_enquiry.txt")
    with right:
        if LOGO: st.image(str(LOGO),use_container_width=True)
        st.markdown('<div class="card"><h3>Pilot conversations</h3><p>We want to learn from supermarket operators, restaurant teams, refrigeration technicians and facility managers. A pilot requires permission to use site data, data-quality review and clear validation criteria.</p><p><b>Current status:</b> early prototype / demonstration software.</p></div>',unsafe_allow_html=True)

elif page=="Live Dashboard":
    hero("Live workspace","Refrigeration performance overview.","Explore simulated readings or upload your own structured CSV to view energy estimates and screening signals.")
    with st.expander("Dashboard settings",expanded=True):
        source=st.radio("Data source",["Demo data","Upload CSV"],horizontal=True)
        a,b,c=st.columns(3)
        with a: tariff=st.number_input("Electricity tariff (₹/kWh)",min_value=0.0,value=8.0,step=.5)
        with b: limit=st.number_input("Temperature deviation limit (°C)",min_value=.5,max_value=20.0,value=2.0,step=.5)
        with c: duration=st.number_input("Consecutive readings for alert",min_value=1,max_value=12,value=2,step=1)
    if source=="Upload CSV":
        upload=st.file_uploader("Upload refrigeration data CSV",type=["csv"])
        if upload is None: st.info("Required columns: "+", ".join(REQUIRED)); st.stop()
        try: df=pd.read_csv(upload)
        except Exception as e: st.error(f"Could not read CSV: {e}"); st.stop()
    else: df=demo_data(); st.caption("Demo mode: all readings are simulated.")
    missing=[c for c in REQUIRED if c not in df.columns]
    if missing: st.error("Missing required columns: "+", ".join(missing)); st.stop()
    df["timestamp"]=pd.to_datetime(df["timestamp"],errors="coerce")
    for col in REQUIRED[1:]: df[col]=pd.to_numeric(df[col],errors="coerce")
    df=df.dropna(subset=REQUIRED).sort_values("timestamp").reset_index(drop=True)
    if df.empty: st.error("No valid rows found. Check your CSV values."); st.stop()
    df["temperature_deviation_c"]=df["room_temperature_c"]-df["setpoint_c"]
    df["energy_kwh"]=df["compressor_power_kw"] # assumes one-hour sampling
    df["estimated_cost_inr"]=df["energy_kwh"]*tariff
    excursion=df["temperature_deviation_c"].abs()>=limit
    groups=(excursion!=excursion.shift()).cumsum()
    df["persistent_temperature_alert"]=excursion&(excursion.groupby(groups).cumsum()>=duration)
    med=df["compressor_power_kw"].median(); mad=(df["compressor_power_kw"]-med).abs().median()
    threshold=med+max(3*1.4826*mad,1.0)
    df["unusual_power"]=df["compressor_power_kw"]>threshold
    energy=float(df["energy_kwh"].sum()); cost=float(df["estimated_cost_inr"].sum()); avg=float(df["compressor_power_kw"].mean())
    ta=int(df["persistent_temperature_alert"].sum()); pa=int(df["unusual_power"].sum())
    a,b,c,d=st.columns(4); a.metric("Estimated energy",f"{energy:,.1f} kWh"); b.metric("Indicative cost",f"₹{cost:,.0f}"); c.metric("Avg compressor power",f"{avg:.2f} kW"); d.metric("Temperature signals",str(ta))
    t1,t2,t3,t4=st.tabs(["Performance","Signals","Energy","Data & export"])
    with t1:
        l,r=st.columns(2)
        with l: st.markdown("#### Room temperature vs setpoint"); st.line_chart(df.set_index("timestamp")[["room_temperature_c","setpoint_c"]],height=300)
        with r: st.markdown("#### Compressor power"); st.line_chart(df.set_index("timestamp")[["compressor_power_kw"]],height=300)
        st.caption("Energy estimate assumes each row represents one hour of average compressor power.")
    with t2:
        alerts=[]
        for _,row in df.iterrows():
            if row["persistent_temperature_alert"]: alerts.append({"Timestamp":row["timestamp"],"Signal":"Persistent temperature deviation","Evidence":f"{row['temperature_deviation_c']:+.1f} °C from setpoint","Suggested check":"Verify sensor, door openings, loading and refrigeration operation."})
            if row["unusual_power"]: alerts.append({"Timestamp":row["timestamp"],"Signal":"Unusual compressor power","Evidence":f"{row['compressor_power_kw']:.2f} kW; threshold {threshold:.2f} kW","Suggested check":"Compare cooling demand and ambient conditions; review condenser cleanliness."})
        if alerts:
            alert_df=pd.DataFrame(alerts); st.warning(f"{len(alerts)} screening signal(s) flagged. These are not confirmed faults.")
            st.dataframe(alert_df,use_container_width=True,hide_index=True)
            st.download_button("Download signal log CSV",alert_df.to_csv(index=False).encode(),"frostwise_signal_log.csv","text/csv")
        else: st.success("No signals triggered under current screening rules.")
    with t3:
        daily=df.set_index("timestamp").resample("D").agg({"energy_kwh":"sum","estimated_cost_inr":"sum"})
        l,r=st.columns(2)
        with l: st.markdown("#### Daily energy (kWh)"); st.bar_chart(daily[["energy_kwh"]])
        with r: st.markdown("#### Daily cost (₹)"); st.bar_chart(daily[["estimated_cost_inr"]])
        reduction=st.slider("Illustrative energy reduction",0,30,10,1,format="%d%%"); saving=energy*reduction/100
        a,b,c=st.columns(3); a.metric("Assumed reduction",f"{reduction}%"); b.metric("Illustrative energy saving",f"{saving:,.1f} kWh"); c.metric("Illustrative cost saving",f"₹{saving*tariff:,.0f}")
        st.caption("Scenario only; not a measured or guaranteed saving.")
    with t4:
        st.dataframe(df,use_container_width=True,hide_index=True)
        st.download_button("Download analyzed CSV",df.to_csv(index=False).encode(),"frostwise_analyzed_data.csv","text/csv")
        report=f"FROSTWISE REFRIGERATION REPORT\nGenerated: {datetime.now().isoformat(timespec='minutes')}\nData source: {'Simulated demo data' if source=='Demo data' else 'User CSV'}\nValid readings: {len(df)}\nEstimated energy: {energy:.2f} kWh (one-hour interval assumption)\nEstimated cost: INR {cost:.2f}\nAverage compressor power: {avg:.2f} kW\nTemperature screening readings: {ta}\nUnusual compressor power readings: {pa}\nPower threshold: {threshold:.2f} kW\nScreening signals are not confirmed faults."
        st.download_button("Download summary report TXT",report,"frostwise_summary_report.txt")

st.markdown('<div class="footer"><b>FROSTWISE</b> &nbsp; · &nbsp; Smart refrigeration solutions<br/>Team: Sudhirsun S · Zain Abbas A · Sundar H · Subramanian M<br/>Monitor · Analyze · Detect · Optimize<br/><small>AI-generated application images are illustrative concepts; no customer deployment is implied.</small></div>',unsafe_allow_html=True)
