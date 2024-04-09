import streamlit as st
import json

def main():
    st.title("Credit Score Tier")

    default_tiers = [
        {"label": "Excellent credit", "minValue": 800},
        {"label": "Very good credit", "minValue": 740},
        {"label": "Good credit", "minValue": 670},
        {"label": "Fair credit", "minValue": 580},
        {"label": "Poor credit", "minValue": 500},
        {"label": "Very poor credit", "minValue": 300}
    ]

    if "tiers" not in st.session_state:
        st.session_state.tiers = default_tiers[:4]  # Initialize with the first 4 tiers

    finance_markup = st.number_input("Finance Markup", value=0.0, format="%.1f", step=None)
    lease_markup = st.number_input("Lease Markup", value=0.0, format="%.5f", step=None)

    num_rows = len(st.session_state.tiers)

    for i in range(num_rows):
        st.subheader(f"Tier {i + 1}")

        st.session_state.tiers[i]["label"] = st.text_input(f"Tier Label", value=st.session_state.tiers[i]["label"], key=f"tier_label_{i}")
        st.session_state.tiers[i]["minValue"] = st.number_input(f"Minimum Credit Score", value=st.session_state.tiers[i]["minValue"],
                                               key=f"min_score_{i}", min_value=300, max_value=850, step=None)

        if "default" not in st.session_state.tiers[i]:
            st.session_state.tiers[i]["default"] = False

        if any(tier.get("default", False) for tier in st.session_state.tiers):
            st.session_state.tiers[i]["default"] = st.checkbox(f"Default Tier", value=st.session_state.tiers[i]["default"], key=f"default_{i}",
                                              disabled=True)
        else:
            st.session_state.tiers[i]["default"] = st.checkbox(f"Default Tier", value=st.session_state.tiers[i]["default"], key=f"default_{i}")

        custom_markup = st.checkbox(f"Custom Markup", key=f"custom_markup_{i}")

        if custom_markup:
            finance_value = st.number_input(f"Custom Finance Value", key=f"finance_value_{i}", format="%.1f", step=None)
            lease_value = st.number_input(f"Custom Lease Value", key=f"lease_value_{i}", format="%.5f", step=None)
        else:
            finance_value = finance_markup
            lease_value = lease_markup

        customize_used = st.checkbox(f"Customize Used Configuration", key=f"customize_used_{i}")

        if customize_used:
            used_finance_value = st.number_input(f"Used Finance Value", key=f"used_finance_value_{i}", format="%.1f", step=None)
            used_lease_value = st.number_input(f"Used Lease Value", key=f"used_lease_value_{i}", format="%.5f", step=None)
        else:
            used_finance_value = finance_value
            used_lease_value = lease_value

        st.session_state.tiers[i]["new"] = {
            "finance": {
                "captive": finance_value,
                "nonCaptive": finance_value
            },
            "lease": {
                "captive": lease_value,
                "nonCaptive": lease_value
            }
        }
        st.session_state.tiers[i]["used"] = {
            "finance": {
                "captive": used_finance_value,
                "nonCaptive": used_finance_value
            },
            "lease": {
                "captive": used_lease_value,
                "nonCaptive": used_lease_value
            }
        }

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Tier"):
            next_tier_index = len(st.session_state.tiers)
            if next_tier_index < len(default_tiers):
                st.session_state.tiers.append(default_tiers[next_tier_index])
            else:
                st.session_state.tiers.append({"label": "", "minValue": 300})
            st.experimental_rerun()

    with col2:
        if st.button("Remove Tier"):
            if len(st.session_state.tiers) > 1:
                st.session_state.tiers.pop()
                st.experimental_rerun()
            else:
                st.warning("At least one tier is required.")

    if st.button("Submit"):
        default_count = sum(tier.get("default", False) for tier in st.session_state.tiers)

        if default_count != 1:
            st.error("Please select a default tier.")
        else:
            json_output = json.dumps(st.session_state.tiers, indent=2)
            st.session_state.json_output = json_output

    if "json_output" in st.session_state:
        st.subheader("Generated JSON")
        st.code(st.session_state.json_output, language='json')


if __name__ == "__main__":
    main()