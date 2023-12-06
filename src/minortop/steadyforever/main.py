import argparse
import logging
import os
import pathlib
import pickle
import time

import jinja2
import openai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_most_recent_pkl():
    bash_glob = f"chat_{'[0-9]' * 9}*.pkl"  # chat_1699976041*.pkl
    pkl_files = list(pathlib.Path(".").glob(bash_glob))
    if not pkl_files:
        return None

    recent = max(pkl_files, key=os.path.getmtime)
    if recent:
        with open(recent, "rb") as file:
            loaded_data = pickle.load(file)
        return loaded_data

    return None


def gen_chat_content():
    sect1 = pathlib.Path("chat_instructions.txt").read_text()
    sect2 = pathlib.Path("chat_recipe.txt").read_text()

    # Use Jinja2 template for combined content
    template_path = "template.tmpl"
    template = jinja2.Template(pathlib.Path(template_path).read_text())

    data = {"sect1": sect1, "sect2": sect2}
    combined_content = template.render(data=data)

    pathlib.Path("chat.txt").write_text(combined_content)
    return combined_content


def generate_chat_completion(client, chat_content):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": chat_content,
            },
        ],
    )
    return completion


def pickle_completion(completion):
    serialized_object = pickle.dumps(completion)
    epoch_timestamp = int(time.time())
    file_name = f"chat_{epoch_timestamp}.pkl"
    out = pathlib.Path(file_name)
    out.write_bytes(serialized_object)
    return completion


def render_template(data, template_path="template.j2"):
    template = jinja2.Template(pathlib.Path(template_path).read_text())
    return template.render(data=data)


def write_to_file(content, output_path="results.txt"):
    with open(output_path, "w") as file:
        file.write(content)


def main():
    parser = argparse.ArgumentParser(description="chat completion")
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Skip cache and generate a new completion.",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose logging (debug level)."
    )
    args = parser.parse_args()

    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    completion = None

    if not args.no_cache:
        completion = load_most_recent_pkl()
        logger.debug("Loaded most recent pickle file.")

    if completion is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        client = openai.OpenAI(api_key=api_key)
        chat_content = gen_chat_content()
        completion = generate_chat_completion(client, chat_content)
        pickle_completion(completion)
        logger.debug("Generated new completion and saved to pickle file.")

    logger.debug("+" * 20)
    logger.debug(completion.choices[0].message)
    logger.debug("-" * 20)

    content = completion.choices[0].message.content
    rendered_content = render_template(data=content)
    write_to_file(rendered_content)


if __name__ == "__main__":
    main()
