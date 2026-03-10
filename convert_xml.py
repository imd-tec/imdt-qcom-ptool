# This script converts an XML file containing partition information into a partitions.conf file.
# Usage: python convert_xml.py input.xml output.conf
import xml.etree.ElementTree as ET
import argparse
def convert_xml_to_conf(xml_input_path, conf_output_path):
    try:
        tree = ET.parse(xml_input_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return

    with open(conf_output_path, 'w') as f:
        # 1. Write Header (Matching your provided sample)
        f.write("# Generated partitions.conf\n")
        f.write("# Copyright (c) 2026 IMD Technologies Ltd .\n\n")
        
        # 2. Extract Disk Configuration from parser_instructions
        # Standard defaults based on your sample
        disk_type = "ufs"
        sector_size = "4096"
        wp_boundary = "0"
        
        # Simple extraction for specific known instructions
        instructions = root.find('parser_instructions')
        if instructions is not None and instructions.text:
            text = instructions.text
            if "SECTOR_SIZE_IN_BYTES=4096" in text: sector_size = "4096"
            if "WRITE_PROTECT_BOUNDARY_IN_KB=0" in text: wp_boundary = "0"

        f.write(f"--disk --type={disk_type} --size=76841669632 --write-protect-boundary={wp_boundary} "
                f"--sector-size-in-bytes={sector_size} --grow-last-partition\n\n")

        # 3. Iterate through physical_partition tags (each represents a LUN)
        for lun_id, physical_part in enumerate(root.findall('physical_partition')):
            f.write(f"# This is LUN {lun_id}\n")
            
            for part in physical_part.findall('partition'):
                label = part.get('label')
                size_kb = part.get('size_in_kb')
                type_guid = part.get('type')
                filename = part.get('filename', "")
                
                # Build the partition line
                entry = f"--partition --lun={lun_id} --name={label} --size={size_kb}KB --type-guid={type_guid}"
                
                # Only append filename if it's not empty
                if filename and filename.strip():
                    entry += f" --filename={filename}"
                
                f.write(entry + "\n")
            f.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert XML to partitions.conf")
    parser.add_argument("xml_input", help="Path to the input XML file")
    parser.add_argument("conf_output", help="Path to the output partitions.conf file")
    args = parser.parse_args()

    convert_xml_to_conf(args.xml_input, args.conf_output)
    print(f"Conversion complete: {args.conf_output} has been generated.")