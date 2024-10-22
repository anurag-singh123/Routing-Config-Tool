import tkinter as tk
from tkinter import ttk, messagebox

# Function to generate the appropriate routing command based on the selection
def generate_command():
    selected_protocol = protocol_var.get()
    selected_subfeature = subfeature_var.get()

    command = ""

    # Static Routing
    if selected_protocol == "Static Routing":
        if selected_subfeature == "Add Static Route":
            command = "ip route <destination_network> <subnet_mask> <next_hop_ip>"
        elif selected_subfeature == "Delete Static Route":
            command = "no ip route <destination_network> <subnet_mask> <next_hop_ip>"
        elif selected_subfeature == "Add Default Route":
            command = "ip route 0.0.0.0 0.0.0.0 <next_hop_ip>"
        elif selected_subfeature == "Add Summary Route":
            command = "ip route <summary_network> <subnet_mask> <next_hop_ip>"

    # OSPF Configuration
    elif selected_protocol == "OSPF":
        if selected_subfeature == "Configure OSPF":
            command = "router ospf <process_id>\n network <network> <wildcard_mask> area <area_id>"
        elif selected_subfeature == "Delete OSPF":
            command = "no router ospf <process_id>"
        elif selected_subfeature == "OSPF Cost Configuration":
            command = "interface <interface>\n ip ospf cost <cost_value>"
        elif selected_subfeature == "OSPF Network Type":
            command = "interface <interface>\n ip ospf network <network_type>"  # (broadcast, non-broadcast, point-to-point)
        elif selected_subfeature == "OSPF Timers":
            command = "router ospf <process_id>\n timers throttle spf <minimum> <maximum> <holdtime>"

    # EIGRP Configuration
    elif selected_protocol == "EIGRP":
        if selected_subfeature == "Configure EIGRP":
            command = "router eigrp <autonomous_system>\n network <network>"
        elif selected_subfeature == "Delete EIGRP":
            command = "no router eigrp <autonomous_system>"
        elif selected_subfeature == "EIGRP Metric Configuration":
            command = "interface <interface>\n ip bandwidth <bandwidth_value>"
        elif selected_subfeature == "EIGRP Passive Interface":
            command = "router eigrp <autonomous_system>\n passive-interface <interface>"
        elif selected_subfeature == "EIGRP Stub Configuration":
            command = "router eigrp <autonomous_system>\n eigrp stub"

    # BGP Configuration
    elif selected_protocol == "BGP":
        if selected_subfeature == "Configure BGP":
            command = "router bgp <asn>\n neighbor <neighbor_ip> remote-as <neighbor_as>"
        elif selected_subfeature == "Delete BGP":
            command = "no router bgp <asn>"
        elif selected_subfeature == "BGP Network Statement":
            command = "router bgp <asn>\n network <network> mask <mask>"
        elif selected_subfeature == "BGP Route Map":
            command = "router bgp <asn>\n neighbor <neighbor_ip> route-map <map_name> in"
        elif selected_subfeature == "BGP Summarization":
            command = "router bgp <asn>\n aggregate-address <summary_network> <mask> summary-only"

    # RIP Configuration
    elif selected_protocol == "RIP":
        if selected_subfeature == "Configure RIP":
            command = "router rip\n version 2\n network <network>"
        elif selected_subfeature == "Delete RIP":
            command = "no router rip"
        elif selected_subfeature == "RIP Passive Interface":
            command = "router rip\n passive-interface <interface>"
        elif selected_subfeature == "RIP Timers":
            command = "router rip\n timers basic <update> <invalid> <hold> <flush>"

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, command)

# Function to update subfeatures based on protocol selection
def update_subfeatures(*args):
    selected_protocol = protocol_var.get()

    subfeatures = []
    if selected_protocol == "Static Routing":
        subfeatures = [
            "Add Static Route",
            "Delete Static Route",
            "Add Default Route",
            "Add Summary Route"
        ]
    elif selected_protocol == "OSPF":
        subfeatures = [
            "Configure OSPF",
            "Delete OSPF",
            "OSPF Cost Configuration",
            "OSPF Network Type",
            "OSPF Timers"
        ]
    elif selected_protocol == "EIGRP":
        subfeatures = [
            "Configure EIGRP",
            "Delete EIGRP",
            "EIGRP Metric Configuration",
            "EIGRP Passive Interface",
            "EIGRP Stub Configuration"
        ]
    elif selected_protocol == "BGP":
        subfeatures = [
            "Configure BGP",
            "Delete BGP",
            "BGP Network Statement",
            "BGP Route Map",
            "BGP Summarization"
        ]
    elif selected_protocol == "RIP":
        subfeatures = [
            "Configure RIP",
            "Delete RIP",
            "RIP Passive Interface",
            "RIP Timers"
        ]

    subfeature_var.set('')  # Clear current subfeature
    subfeature_menu['values'] = subfeatures  # Update values for subfeature menu
    
    if subfeatures:  # Ensure there's at least one option
        subfeature_var.set(subfeatures[0])  # Set the first subfeature as the default

# Function to copy to clipboard
def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(output_text.get(1.0, tk.END))
    messagebox.showinfo("Copied", "Command copied to clipboard!")

# Main window
root = tk.Tk()
root.title("CiscoConfigGen - Routing Configuration Generator")

# Dropdown for protocol selection
protocol_var = tk.StringVar(root)
protocol_var.set("Select Routing Protocol")
protocol_label = tk.Label(root, text="Select Routing Protocol:")
protocol_label.pack(pady=5)

protocols = [
    "Static Routing",
    "OSPF",
    "EIGRP",
    "BGP",
    "RIP"
]

protocol_menu = ttk.Combobox(root, textvariable=protocol_var, values=protocols)
protocol_menu.pack(pady=5)
protocol_menu.bind("<<ComboboxSelected>>", update_subfeatures)

# Dropdown for sub-feature selection
subfeature_var = tk.StringVar(root)
subfeature_var.set("Select Routing Command")

subfeature_label = tk.Label(root, text="Select Routing Command:")
subfeature_label.pack(pady=5)

subfeature_menu = ttk.Combobox(root, textvariable=subfeature_var)
subfeature_menu.pack(pady=5)

# Button to generate the command
generate_button = tk.Button(root, text="Generate Command", command=generate_command)
generate_button.pack(pady=10)

# Textbox for output
output_text = tk.Text(root, height=10, width=60)
output_text.pack(pady=10)

# Copy button
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack()

root.mainloop()
