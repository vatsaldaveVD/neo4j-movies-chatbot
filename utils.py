def format_results(results) -> str:
    if not results:
        return "No results found."

    formatted_results = []

    for record in results:
        parts = []
        for key, value in record.items():
            if hasattr(value, "labels"):  # Node
                labels = ":".join(value.labels)
                props = dict(value.items())
                display_props = []
                if "name" in props:
                    display_props.append(f"name: {props['name']}")
                elif "title" in props:
                    display_props.append(f"title: {props['title']}")
                if "year" in props:
                    display_props.append(f"year: {props['year']}")
                if "born" in props:
                    display_props.append(f"born: {props['born']}")
                if "imdbRating" in props:
                    display_props.append(f"rating: {props['imdbRating']}")
                prop_str = (
                    ", ".join(display_props) if display_props else "properties present"
                )
                parts.append(f"({labels} {{{prop_str}}})")

            elif hasattr(value, "type"):  # Relationship
                rel_type = value.type
                rel_props = dict(value.items())
                prop_str = (
                    ", ".join(f"{k}: {v}" for k, v in rel_props.items())
                    if rel_props
                    else "no properties"
                )
                start = value.start_node
                end = value.end_node
                start_label = ":".join(start.labels) if start else "Node"
                end_label = ":".join(end.labels) if end else "Node"
                start_name = (
                    start.get("name") or start.get("title") if start else "start"
                )
                end_name = end.get("name") or end.get("title") if end else "end"
                parts.append(
                    f"({start_label} '{start_name}')-[:{rel_type} {{{prop_str}}}]->({end_label} '{end_name}')"
                )

            else:
                parts.append(f"{key}: {value}")

        formatted_results.append("; ".join(parts))

    return "\n\n".join(formatted_results)
