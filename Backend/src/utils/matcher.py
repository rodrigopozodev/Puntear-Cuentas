def complete_matching(debe_data, haber_data):
    matched_pairs = []
    for debe_entry in debe_data:
        for haber_entry in haber_data:
            if debe_entry['amount'] == haber_entry['amount']:
                matched_pairs.append((debe_entry, haber_entry))
                break
    return matched_pairs

def debe_matching(debe_data, haber_data):
    matched_pairs = []
    for debe_entry in debe_data:
        total_debe = sum(entry['amount'] for entry in debe_data)
        for haber_entry in haber_data:
            if total_debe == haber_entry['amount']:
                matched_pairs.append((debe_entry, haber_entry))
                break
    return matched_pairs

def haber_matching(debe_data, haber_data):
    matched_pairs = []
    for haber_entry in haber_data:
        total_haber = sum(entry['amount'] for entry in haber_data)
        for debe_entry in debe_data:
            if total_haber == debe_entry['amount']:
                matched_pairs.append((debe_entry, haber_entry))
                break
    return matched_pairs