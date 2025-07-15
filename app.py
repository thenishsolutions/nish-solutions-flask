import os
import re
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_very_secure_secret_for_the_nish_solutions'

def generate_advanced_report(risk_description, industry, company_size):
    """
    This function simulates a call to a generative AI model.
    It builds a report by analyzing keywords in the user's input.
    """
    # --- High-Level Prompt for a Real GenAI Model ---
    # This is the kind of detailed prompt you would send to a powerful LLM.
    # """
    # You are an expert cybersecurity and risk management consultant. Your task is to generate a comprehensive, professional, and actionable risk mitigation report based on the user's input.
    #
    # **User Input:**
    # - Risk Description: "{risk_description}"
    # - Industry: "{industry}"
    # - Company Size: "{company_size}"
    #
    # **Report Structure and Tone:**
    # The report should be structured, formal, and tailored. Avoid generic statements. Use clear headings with markdown for emphasis (**Bold**).
    #
    # **Instructions:**
    # 1.  **Executive Summary:** Start with a brief, high-level overview of the identified risk and the core of the mitigation strategy.
    # 2.  **Threat Analysis:** Briefly analyze the risk in the context of the provided industry and company size. What are the likely threat actors and impacts?
    # 3.  **Recommended Mitigation Strategies:** This is the main section. Divide it into three clear sub-sections:
    #     a.  **Technical Controls:** Specific, actionable technical solutions.
    #     b.  **Administrative Controls:** Policies, procedures, and training.
    #     c.  **Physical Controls:** If applicable, controls for physical security.
    # 4.  **Compliance & Regulatory Considerations:** If the industry is specified (e.g., Healthcare, Finance), mention relevant regulations (e.g., HIPAA, GDPR, PCI-DSS) and how the mitigations help with compliance.
    # 5.  **Implementation Roadmap (Prioritization):** Suggest a phased approach (e.g., Phase 1: Critical, Phase 2: Important, Phase 3: Long-term) for implementing the controls, considering the company size (startups need a more budget-focused roadmap).
    #
    # **Tailoring Logic:**
    # - If the risk involves "data breach," "exfiltration," or "unauthorized access," focus on data loss prevention (DLP), encryption, and access control.
    # - If the risk is "insider threat," emphasize user activity monitoring, RBAC, and offboarding procedures.
    # - If the risk is "ransomware," prioritize backups, network segmentation, and EDR.
    # - For "Startups" or "Small Businesses," suggest open-source or cost-effective solutions and prioritize fundamental controls.
    # - For "Large Enterprises," recommend scalable, enterprise-grade solutions and more formal governance structures.
    # """

    report_parts = []
    risk_lower = risk_description.lower()
    industry_lower = industry.lower()
    size_lower = company_size.lower()

    # 1. Executive Summary
    report_parts.append(
        "**Executive Summary**\n"
        f"This report outlines a strategic mitigation plan for the identified risk: '{risk_description}'. "
        "The recommended approach integrates a defense-in-depth strategy, combining technical, administrative, and physical controls tailored to a "
        f"{company_size}-sized company in the {industry} sector. The goal is to reduce the risk's likelihood and potential impact to an acceptable level."
    )

    # 2. Threat Analysis
    analysis = [
        "**Threat Analysis**\n"
        "Based on the provided context, the primary threat actors could range from opportunistic cybercriminals to sophisticated, targeted attackers."
    ]
    if 'insider' in risk_lower:
        analysis.append("A key concern is the potential for malicious or unintentional actions by privileged insiders, who have legitimate access to sensitive systems.")
    if 'ransomware' in risk_lower:
        analysis.append("Ransomware attacks are a significant threat, potentially leading to operational disruption, data loss, and severe financial and reputational damage.")
    if 'phishing' in risk_lower or 'social engineering' in risk_lower:
        analysis.append("Social engineering remains a primary vector for initial access. Employees are a critical control point and potential vulnerability.")
    analysis.append(f"For a company of your size and industry, the impact could range from regulatory fines to loss of customer trust and business continuity.")
    report_parts.append("\n".join(analysis))

    # 3. Recommended Mitigation Strategies
    technical = [
        "**1. Technical Controls**",
        "   - **Access Management:** Implement and enforce a strict Role-Based Access Control (RBAC) model based on the principle of least privilege. Regularly review and recertify access rights.",
        "   - **Endpoint Security:** Deploy a modern Endpoint Detection and Response (EDR) solution. Ensure it is configured for behavioral analysis to detect anomalous activity.",
        "   - **Data Encryption:** Encrypt all sensitive data, both at rest (e.g., AES-256 for databases) and in transit (e.g., TLS 1.3 for network traffic)."
    ]
    if 'ransomware' in risk_lower:
        technical.append("   - **Backup and Recovery:** Maintain immutable, offline backups of critical data (3-2-1 rule). Regularly test restoration procedures to ensure viability.")
    if 'insider' in risk_lower or 'data' in risk_lower or 'exfiltration' in risk_lower:
        technical.append("   - **Data Loss Prevention (DLP):** Implement a DLP solution to monitor, detect, and block unauthorized data exfiltration through email, USB drives, and cloud services.")

    administrative = [
        "**2. Administrative Controls**",
        "   - **Information Security Policies:** Develop, approve, and disseminate a comprehensive set of security policies. These must be reviewed at least annually.",
        "   - **Security Awareness Training:** Conduct mandatory, ongoing training for all staff. Use phishing simulations to test and reinforce learning.",
        "   - **Incident Response (IR) Plan:** Establish a formal IR plan with clear roles, responsibilities, and communication channels. Conduct tabletop exercises to test the plan's effectiveness."
    ]
    if 'insider' in risk_lower:
        administrative.append("   - **Employee Offboarding:** Implement a robust offboarding process that ensures timely revocation of all physical and logical access upon an employee's departure.")

    physical = [
        "**3. Physical Controls**",
        "   - **Facility Security:** Secure all office locations and data centers with access controls (e.g., badge readers). Maintain logs of physical access.",
        "   - **Clean Desk Policy:** Enforce a clean desk policy to prevent sensitive information from being left unattended in plain sight."
    ]
    
    mitigations = "\n\n".join(["\n".join(technical), "\n".join(administrative), "\n".join(physical)])
    report_parts.append("**Recommended Mitigation Strategies**\n" + mitigations)

    # 4. Compliance Considerations
    compliance = ["**Compliance & Regulatory Considerations**"]
    if 'health' in industry_lower:
        compliance.append("   - **HIPAA:** The recommended controls, particularly around access management and encryption, are critical for maintaining compliance with the Health Insurance Portability and Accountability Act (HIPAA) Security Rule.")
    elif 'fin' in industry_lower or 'bank' in industry_lower:
        compliance.append("   - **GLBA/PCI-DSS:** For financial institutions, these controls support compliance with the Gramm-Leach-Bliley Act (GLBA) and, if payment cards are processed, the Payment Card Industry Data Security Standard (PCI-DSS).")
    else:
        compliance.append("   - Ensure all implemented controls align with general data protection regulations such as GDPR or CCPA, depending on your customer base. A formal risk assessment can map controls to specific regulatory requirements.")
    report_parts.append("\n".join(compliance))
    
    # 5. Implementation Roadmap
    roadmap = ["**Implementation Roadmap (Prioritization)**"]
    if 'start' in size_lower or 'small' in size_lower or 'smb' in size_lower:
        roadmap.extend([
            "   - **Phase 1 (0-3 Months - Critical Foundations):** Focus on essentials like multi-factor authentication (MFA) everywhere, security awareness training, and a robust backup/recovery system.",
            "   - **Phase 2 (3-9 Months - Hardening):** Implement RBAC, develop the formal IR plan, and deploy a baseline EDR solution.",
            "   - **Phase 3 (9+ Months - Maturity):** Explore advanced solutions like DLP and conduct regular penetration testing."
        ])
    else: # Assume medium to large enterprise
        roadmap.extend([
            "   - **Phase 1 (0-6 Months - Foundational & High-Risk):** Immediately deploy EDR and DLP across all endpoints. Solidify IR plan and conduct initial tabletop exercises. Enforce RBAC and conduct an access review.",
            "   - **Phase 2 (6-12 Months - Enhancement & Governance):** Mature the security training program with advanced phishing sims. Integrate security tools into a SIEM for centralized monitoring. Formalize policy governance and review cycles.",
            "   - **Phase 3 (12+ Months - Proactive Defense):** Establish a threat intelligence program. Conduct regular, advanced adversary simulation (red teaming) exercises to test defenses."
        ])
    report_parts.append("\n".join(roadmap))
    
    return "\n\n".join(report_parts)

def format_report_for_html(text):
    """Converts a markdown-like text to HTML."""
    # Convert markdown-style bold to <strong> tags
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Convert newlines to <br> tags for HTML rendering
    text = text.replace('\n', '<br>')
    return text

@app.route('/', methods=['GET', 'POST'])
def mitigation_tool():
    if request.method == 'POST':
        risk_description = request.form.get('risk_description', 'No description provided.')
        industry = request.form.get('industry') if request.form.get('industry') else 'General Business'
        company_size = request.form.get('company_size') if request.form.get('company_size') else 'Medium-Sized Business'
        
        # In a real app, you would have your AI logic here.
        # This is a placeholder response.
        raw_report = generate_advanced_report(risk_description, industry, company_size)
        
        # Format the report for clean HTML display
        result_text = format_report_for_html(raw_report)
        return render_template('mitigation_tool.html', result=result_text)

    # For GET requests, just render the page without results
    return render_template('mitigation_tool.html', result=None)

if __name__ == '__main__':
    # This block is for local development. Render will use the Gunicorn command.
    port = int(os.environ.get('PORT', 5004))
    app.run(host='0.0.0.0', port=5005, debug=True)
