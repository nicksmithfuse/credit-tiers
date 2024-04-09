import streamlit as st
import json

def main():
    st.title("Credit Score Tier Form")

    tiers = [
        {"label": "Excellent credit", "minValue": 800},
        {"label": "Very good credit", "minValue": 740},
        {"label": "Good credit", "minValue": 670},
        {"label": "Fair credit", "minValue": 580}
    ]

    finance_markup = st.number_input("Finance Markup", value=0.0, format="%.1f")
    lease_markup = st.number_input("Lease Markup", value=0.0, format="%.5f")

    num_rows = len(tiers)

    for i in range(num_rows):
        st.subheader(f"Tier {i + 1}")

        tiers[i]["label"] = st.text_input(f"Tier Label", value=tiers[i]["label"], key=f"tier_label_{i}")
        tiers[i]["minValue"] = st.number_input(f"Minimum Credit Score", value=tiers[i]["minValue"],
                                               key=f"min_score_{i}", min_value=300, max_value=850, step=1)

        if "default" not in tiers[i]:
            tiers[i]["default"] = False

        if any(tier.get("default", False) for tier in tiers):
            tiers[i]["default"] = st.checkbox(f"Default Tier", value=tiers[i]["default"], key=f"default_{i}",
                                              disabled=True)
        else:
            tiers[i]["default"] = st.checkbox(f"Default Tier", value=tiers[i]["default"], key=f"default_{i}")

        custom_markup = st.checkbox(f"Custom Markup", key=f"custom_markup_{i}")

        if custom_markup:
            finance_value = st.number_input(f"Custom Finance Value", key=f"finance_value_{i}", format="%.1f")
            lease_value = st.number_input(f"Custom Lease Value", key=f"lease_value_{i}", format="%.5f")
        else:
            finance_value = finance_markup
            lease_value = lease_markup

        customize_used = st.checkbox(f"Customize Used Configuration", key=f"customize_used_{i}")

        if customize_used:
            used_finance_value = st.number_input(f"Used Finance Value", key=f"used_finance_value_{i}", format="%.1f")
            used_lease_value = st.number_input(f"Used Lease Value", key=f"used_lease_value_{i}", format="%.5f")
        else:
            used_finance_value = finance_value
            used_lease_value = lease_value

        tiers[i]["new"] = {
            "finance": {
                "captive": finance_value,
                "nonCaptive": finance_value
            },
            "lease": {
                "captive": lease_value,
                "nonCaptive": lease_value
            }
        }
        tiers[i]["used"] = {
            "finance": {
                "captive": used_finance_value,
                "nonCaptive": used_finance_value
            },
            "lease": {
                "captive": used_lease_value,
                "nonCaptive": used_lease_value
            }
        }

    if st.button("Add Tier"):
        num_rows += 1
        tiers.insert(0, {"label": "", "minValue": 0})
        st.experimental_rerun()

    if st.button("Submit"):
        default_count = sum(tier.get("default", False) for tier in tiers)

        if default_count != 1:
            st.error("Please select exactly one tier as the default.")
        else:
            json_output = json.dumps(tiers, indent=2)
            st.session_state.json_output = json_output
            st.experimental_rerun()

    if "json_output" in st.session_state:
        st.subheader("Generated JSON")
        st.code(st.session_state.json_output, language='json')


if __name__ == "__main__":
    main()