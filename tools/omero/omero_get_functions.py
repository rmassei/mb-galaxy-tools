import argparse

import ezomero as ez
import pandas as pd


def filter_objects_omero(user, pws, host, port, obj, id=None, output_file="output.csv"):
    # Connect to OMERO
    conn = ez.connect(user, pws, "", host, port, secure=True)

    try:
        # Fetch the data based on object type
        if obj == "comment":
            if id is None:
                raise ValueError("ID is required for comment object type.")
            result = ez.get_comment_annotation(conn, id)
            print(result)
        elif obj == "dataset":
            if id is None:
                raise ValueError("ID is required for dataset object type.")
            dataset_ids = ez.get_dataset_ids(conn, project=id)
            df = pd.DataFrame(dataset_ids, columns=['Dataset_ID'])
            df.to_csv(output_file, index=False)
            print(f"Output saved to {output_file}")
        elif obj == "image":
            if id is None:
                raise ValueError("ID is required for image object type.")
            image_ids = ez.get_image_ids(conn, dataset=id)
            df = pd.DataFrame(image_ids, columns=['Image_ID'])
            df.to_csv(output_file, index=False)
            print(f"Output saved to {output_file}")
        elif obj == "object":
            if id is None:
                raise ValueError("ID is required for object object type.")
            result = ez.get_map_annotation(conn, id)
            print(result)
        elif obj == "project":
            project_ids = ez.get_project_ids(conn)
            df = pd.DataFrame(project_ids, columns=['Project_ID'])
            df.to_csv(output_file, index=False)
            print(f"Output saved to {output_file}")
        elif obj == "table":
            if id is None:
                raise ValueError("ID is required for table object type.")
            result = ez.get_table(conn, id)
            print(result)
        elif obj == "tag":
            if id is None:
                raise ValueError("ID is required for tag object type.")
            result = ez.get_tag(conn, id)
            print(result)
        else:
            print(f"Invalid object type: {obj}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Filter OMERO objects and save the output to a file.")
    parser.add_argument("user", help="OMERO username")
    parser.add_argument("pws", help="OMERO password")
    parser.add_argument("host", help="OMERO host")
    parser.add_argument("port", type=int, help="OMERO port")
    parser.add_argument("obj", help="Object type (comment, dataset, image, object, project, table, tag)")
    parser.add_argument("--id", type=int, help="Object ID")
    parser.add_argument("--output_file", default="output.csv", help="Output file name (default: output.csv)")

    args = parser.parse_args()

    filter_objects_omero(args.user, args.pws, args.host, args.port, args.obj, args.id, args.output_file)


if __name__ == "__main__":
    main()


