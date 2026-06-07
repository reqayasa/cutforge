import csv

DEMAND_HEADER_ALIASES = {
    "id": {
        "id",
        "part",
        "part_id",
        "partid",
        "id_part",
        "mark",
        "name",
    },

    "group": {
        "group",
        "category",
        "type",
        "section",
    },

    "length": {
        "length",
        "len",
        "panjang",
        "cut_length",
    },

    "quantity": {
        "qty",
        "quantity",
        "jumlah",
        "count",
        "pcs",
    },
}

REQUIRED_FIELDS = {
    "length",
    "quantity",
}


def read_csv(path: str) -> list[tuple]:

    with open (path, mode='r', newline = "") as csvfile:
        reader = csv.DictReader(csvfile)

        # Extract the first row as the header
        header = reader.fieldnames
        
        body = list(reader)

        return (header, body) 
    
def normalize_header(text: str) -> str:
    return (
        text.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

def resolve_headers(
        csv_headers: list[str],
        aliases: dict[str, set[str]],
    ) -> dict[str, str]:

    resolved = {}

    normalized_headers = {
        normalize_header(h): h
        for h in csv_headers
    }

    for field, valid_aliases in aliases.items():
        for alias in valid_aliases:
            if alias in normalized_headers:
                resolved[field] = normalized_headers[alias]
                break

    return resolved

def parse_row(
        row: dict[str, str],
        mapping: dict[str, str],
        data_type
    ):

        return data_type(
            id=row.get(mapping.get("id", ""), ""),
            group=row.get(mapping.get("group", ""), ""),
            length=row.get(mapping["length"], ""),
            quantity=row.get(mapping["quantity"], ""),
    )
        
