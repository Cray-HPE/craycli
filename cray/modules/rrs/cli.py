""" rrs """
# pylint: disable=invalid-name
from cray.generator import generate
from cray import formatting
import json
# from tabulate import tabulate 
def make_table(headers, rows):
    """
    Given a list of headers and a list of rows (each a list of stringable items),
    returns a string representing the table.
    """
    # Compute the maximum width of each column
    widths = [len(str(header)) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    # Create the header line
    header_line = " | ".join(str(header).ljust(widths[i]) for i, header in enumerate(headers))
    # Create a separator line
    separator_line = "-+-".join("-" * widths[i] for i in range(len(headers)))
    
    # Build the table lines
    lines = [header_line, separator_line]
    for row in rows:
        line = " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))
        lines.append(line)
    
    return "\n".join(lines)


def format_rrs_response(result, **kwargs):
    """
    Callback function to format RRS output into a table.
    
    Expects 'result' to be a dict mapping rack names to lists of node dictionaries.
    """
    # If result is a requests.Response, try to decode as JSON.
    if hasattr(result, "json"):
        try:
            result = result.json()
            print(result)
        except Exception:
            result = result.text

    # Ensure result is a dict.
    if not isinstance(result, dict):
        raise ValueError("Expected a dict as the response for RRS zones list")

    output_lines = []
    # Define the order and headers for columns
    headers = ["Name", "Age", "CPU", "Memory", "Roles", "Status", "Version"]
    
    # Iterate over each rack and its node list.
    for rack, nodes in result.items():
        output_lines.append(f"Rack: {rack}")
        table = []
        for node in nodes:
            # Create a row; use get() so missing keys don’t crash
            row = [
                node.get("name", ""),
                node.get("age", ""),
                node.get("cpu", ""),
                node.get("memory", ""),
                node.get("roles", ""),
                node.get("status", ""),
                node.get("version", ""),
            ]
            table.append(row)
        # Format the table (using tabulate for pretty printing)
        # output_lines.append(tabulate(table, headers=headers, tablefmt="grid"))
        output_lines.append(make_table(headers, table))
        output_lines.append("")  # blank line between racks
    # Join all lines and return
    return "\n".join(output_lines)


# Pass the callback to generate()
cli = generate(__file__, callback=format_rrs_response)