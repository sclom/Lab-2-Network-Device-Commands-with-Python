import os
import json
import logging

def generate_report():
    structured_dir = os.path.join('data', 'structured')
    reports_dir = os.path.join('data', 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    def load_json(filename):
        path = os.path.join(structured_dir, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    version_data = load_json('show_version.json')
    ip_brief_data = load_json('show_ip_interface_brief.json')
    inventory_data = load_json('show_inventory.json')

    hostname = "Unknown"
    model = "Unknown"
    version = "Unknown"

    if version_data and isinstance(version_data, list) and len(version_data) > 0:
        v_info = version_data[0]
        hostname = v_info.get('hostname', 'Unknown')
        version = v_info.get('version', 'Unknown')
        hardware_list = v_info.get('hardware', [])
        if isinstance(hardware_list, list) and hardware_list:
            model = hardware_list[0]

    if model == "Unknown" and isinstance(inventory_data, list):
        model = next(
            (item.get('pid') for item in inventory_data if item.get('pid')),
            "Unknown",
        )

    if not isinstance(ip_brief_data, list):
        ip_brief_data = []
    total_interfaces = len(ip_brief_data)
    up_interfaces = 0
    down_interfaces = 0

    interface_lines = []
    if ip_brief_data:
        for intf in ip_brief_data:
            name = intf.get('interface', 'N/A')
            ip = intf.get('ip_address', 'Unassigned')
            status = str(intf.get('status') or 'down').lower()
            protocol = str(intf.get('proto') or 'down').lower()

            if 'up' in status:
                up_interfaces += 1
            else:
                down_interfaces += 1

            interface_lines.append(f" - Interface: {name:<15} IP: {ip:<15} Status: {status} / {protocol}")

    report_content = f"""
Hostname: {hostname}
Model: {model}
Version: {version}

Total Interfaces: {total_interfaces}
Up Interfaces: {up_interfaces}
Down Interfaces: {down_interfaces}

Interface Details:
{chr(10).join(interface_lines[:10]) if interface_lines else "  - No interface data available."}
"""
    print(report_content)
    report_path = os.path.join(reports_dir, f"{hostname}_report.txt")
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
    except OSError:
        logging.exception("Failed to save device summary report.")
        raise
    logging.info("[REPORT_SAVED]")

    return report_path