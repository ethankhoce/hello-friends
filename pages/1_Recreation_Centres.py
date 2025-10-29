import streamlit as st


def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)


def _display_disclaimer() -> None:
    """Display the disclaimer notice at the top of the page"""
    st.markdown("""
        <div style="background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 1rem; margin-bottom: 1.5rem; border-radius: 5px;">
            <h4 style="margin: 0 0 0.5rem 0; color: #856404;">⚠️ IMPORTANT NOTICE</h4>
            <p style="margin: 0; color: #856404;">
                <strong>This web application is a prototype developed for educational purposes only.</strong> The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #856404;">
                Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #856404;">
                Always consult with qualified professionals for accurate and personalized advice.
            </p>
        </div>
        """, unsafe_allow_html=True)


def _section_heading(title: str, emoji: str = "") -> None:
    if emoji:
        st.markdown(f"### {emoji} {title}")
    else:
        st.markdown(f"### {title}")


def _format_link(label: str, url: str) -> str:
    return f"[{label}]({url})"


def main() -> None:
    if not check_authentication():
        st.error("🔒 Please log in to access this page.")
        st.info("Go to the main page to log in.")
        st.stop()
    
    _display_disclaimer()
    
    st.markdown(
        """
        <div style="text-align: center; padding: 1.5rem 0; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 1.5rem;">
            <h1 style="margin: 0; font-size: 2.2rem;">Recreation centres for migrant workers</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9;">Addresses, hours, facilities and booking links</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _section_heading("Centres & facilities", "🏟️")

    centres = [
        {
            "name": "Kaki Bukit RC",
            "address": "7 Kaki Bukit Ave 3 Singapore 415814",
            "map": "https://www.onemap.gov.sg/?lat=1.3372047&lng=103.9068736",
            "phone": "tel:68422995",
            "hours": "Mon–Sun 7.00am–10.30pm",
            "booking": "Walk-in",
            "booking_url": "",
            "facilities": "Badminton, Basketball, Futsal, Sepak takraw, Volleyball",
        },
        {
            "name": "Kranji RC",
            "address": "11 Kranji Close Singapore 737673",
            "map": "https://www.onemap.gov.sg/?lat=1.4281351&lng=103.7533114",
            "phone": "tel:62981247",
            "hours": "Mon–Sun 8.00am–11.30pm",
            "booking": "FWMOMCare",
            "booking_url": "/eservices/fwmomcare",
            "facilities": "Badminton, Basketball, Carrom, Cricket lane, Futsal, Indoor kabaddi, Multi-purpose room, Sepak takraw, Soccer field, Volleyball",
        },
        {
            "name": "Penjuru RC",
            "address": "27 Penjuru Walk Singapore 608538",
            "map": "https://www.onemap.gov.sg/?lat=1.3192382&lng=103.7328825",
            "phone": "tel:68980493",
            "hours": "Mon–Sun 8.00am–11.30pm",
            "booking": "FWMOMCare",
            "booking_url": "/eservices/fwmomcare",
            "facilities": "Badminton, Basketball, Carrom, Cricket lane, Futsal, Multi-purpose hall, Sepak takraw, Soccer field, Volleyball",
        },
        {
            "name": "Migrant Workers' Centre Recreation Club",
            "address": "51 Soon Lee Rd Singapore 628088",
            "map": "https://www.onemap.gov.sg/?lat=1.332637&lng=103.6991344",
            "phone": "tel:65362692",
            "hours": "Mon 8.00am–6.00pm; Tue–Sat 8.00am–7.00pm; Sun 11.00am–3.00pm",
            "booking": "MWC Facility Booking Portal",
            "booking_url": "https://www.mwcrc.com/Account/Login?ReturnUrl=%2F",
            "facilities": "Amphitheatre, Badminton, Beer garden, Cricket field, Futsal, Multi-purpose hall, Sepak takraw, Volleyball",
        },
        {
            "name": "Sembawang RC",
            "address": "301 Canberra Road Singapore 759774",
            "map": "https://www.onemap.gov.sg/?lat=1.4584653&lng=103.8217987",
            "phone": "tel:63227573",
            "hours": "Mon–Sun 8.00am–11.30pm",
            "booking": "FWMOMCare",
            "booking_url": "/eservices/fwmomcare",
            "facilities": "Barbeque pits, Basketball, Carrom, Futsal, Multi-purpose hall, Multi-purpose room, Volleyball",
        },
        {
            "name": "Terusan RC",
            "address": "1 Jalan Papan Singapore 619392",
            "map": "https://www.onemap.gov.sg/?lat=1.3204843&lng=103.7267229",
            "phone": "tel:62641342",
            "hours": "Mon–Sun 8.00am–11.30pm",
            "booking": "FWMOMCare",
            "booking_url": "/eservices/fwmomcare",
            "facilities": "Badminton, Basketball, Carrom, Cricket field, Cricket lane, Fitness corner, Kabaddi field, Multi-purpose hall, Multi-purpose room, Soccer field, Table tennis, Volleyball",
        },
        {
            "name": "Tuas South RC",
            "address": "12 Tuas South Street 13  Singapore 636937",
            "map": "https://www.onemap.gov.sg/?lat=1.2703098&lng=103.634164",
            "phone": "tel:65703121",
            "hours": "Mon–Sun 8.00am–11.30pm",
            "booking": "FWMOMCare",
            "booking_url": "/eservices/fwmomcare",
            "facilities": "Badminton, Carrom, Cricket lane, Multi-purpose hall, Pool table, Soccer field, Sepak takraw, Table tennis, Volleyball",
        },
        {
            "name": "Woodlands RC",
            "address": "200 Woodlands Industrial Park E7 Singapore 757177",
            "map": "https://www.onemap.gov.sg/?lat=1.4507498&lng=103.7968466",
            "phone": "tel:63686845",
            "hours": "Mon–Sun 7.30am–11.00pm",
            "booking": "Walk-in",
            "booking_url": "",
            "facilities": "Amphitheatre/tentage, Basketball, Multi-purpose sports arena, Sepak takraw, Volleyball",
        },
    ]

    # Search bar
    query = st.text_input(
        "Search by name, address, or postal code",
        value="",
        placeholder="e.g. Kranji, Canberra, 415814",
    ).strip()

    def _matches_query(centre: dict, q: str) -> bool:
        if not q:
            return True
        q_lower = q.lower()
        name_lower = (centre["name"] or "").lower()
        addr_lower = (centre["address"] or "").lower()

        # Exact substring
        if q_lower in name_lower or q_lower in addr_lower:
            return True

        # Postal code: keep digits only and look for the digits of q
        import re
        from difflib import SequenceMatcher

        q_digits = re.sub(r"\D", "", q)
        if q_digits:
            addr_digits = re.sub(r"\D", "", centre["address"]) if centre["address"] else ""
            if q_digits and q_digits in addr_digits:
                return True

        # Fuzzy matching: compare against name and address words and whole strings
        def _ratio(a: str, b: str) -> float:
            return SequenceMatcher(None, a, b).ratio()

        # Whole string similarity threshold
        if _ratio(q_lower, name_lower) >= 0.78 or _ratio(q_lower, addr_lower) >= 0.78:
            return True

        # Token-level similarity: match any token closely
        tokens = re.findall(r"[a-z0-9]+", name_lower + " " + addr_lower)
        for tok in tokens:
            if _ratio(q_lower, tok) >= 0.82:
                return True

        return False

    # Facilities filter chips (multiselect)
    def _facility_list(centre: dict) -> list[str]:
        return [s.strip() for s in (centre.get("facilities") or "").split(",") if s.strip()]

    all_facilities = sorted({f for c in centres for f in _facility_list(c)})
    selected_facilities = st.multiselect(
        "Filter by facilities",
        options=all_facilities,
        default=[],
        placeholder="Select facilities...",
    )

    def _matches_facilities(centre: dict) -> bool:
        if not selected_facilities:
            return True
        centre_fac = set(_facility_list(centre))
        # Match any selected facility
        return any(f in centre_fac for f in selected_facilities)

    filtered = [c for c in centres if _matches_query(c, query) and _matches_facilities(c)]

    # Present as a styled list (cards)
    st.markdown(
        """
        <style>
        .rc-card { border: 1px solid #e6e6e6; border-radius: 12px; padding: 14px; margin-bottom: 12px; background: #fff; }
        .rc-header { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
        .rc-title { font-size: 1.05rem; font-weight: 700; margin: 0; }
        .rc-sub { color: #555; margin: 2px 0 0 0; font-size: 0.92rem; }
        .rc-meta { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 6px 14px; margin-top: 10px; }
        .rc-meta span { display: inline-flex; align-items: center; gap: 6px; color: #444; font-size: 0.9rem; }
        .rc-chips { margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px; }
        .rc-chip { background: #f3f4f6; color: #374151; border-radius: 999px; padding: 4px 10px; font-size: 0.85rem; }
        .rc-actions { margin-top: 10px; display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
        .rc-btn { display: inline-block; background: #2563eb; color: #fff !important; padding: 6px 10px; border-radius: 8px; text-decoration: none; font-size: 0.9rem; }
        .rc-link { color: #2563eb !important; text-decoration: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.caption(f"Showing {len(filtered)} of {len(centres)} centres")

    for c in filtered:
        name_link = c["map"] and f"<a class='rc-link' href='{c['map']}' target='_blank' rel='noopener'>{c['name']}</a>" or c["name"]
        booking_html = (
            f"<a class='rc-btn' href='{c['booking_url']}' target='_blank' rel='noopener'>{c['booking']}</a>"
            if c["booking_url"] else f"<span class='rc-chip'>{c['booking']}</span>"
        )
        phone_display = c["phone"].replace("tel:", "") if c["phone"] else ""
        phone_html = phone_display and f"<a class='rc-link' href='{c['phone']}'>{phone_display}</a>" or ""
        chips = [s.strip() for s in c["facilities"].split(",")]
        chips_html = "".join([f"<span class='rc-chip'>{chip}</span>" for chip in chips if chip])

        st.markdown(
            f"""
            <div class="rc-card">
              <div class="rc-header">
                <h3 class="rc-title">{name_link}</h3>
              </div>
              <p class="rc-sub">{c['address']}</p>
              <div class="rc-meta">
                <span>🕒 <strong>Hours:</strong> {c['hours']}</span>
                <span>📞 <strong>Phone:</strong> {phone_html}</span>
              </div>
              <div class="rc-actions">
                {booking_html}
                {c['map'] and f"<a class='rc-link' href='{c['map']}' target='_blank' rel='noopener'>Open map</a>" or ''}
              </div>
              <div class="rc-chips">{chips_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()


# For Streamlit pages, execute main() when module is loaded
main()


