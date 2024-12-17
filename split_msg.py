import click
from html_fragmentor import split_message
from html_fragmentor import MAX_LEN

@click.command()
@click.option('--max-len', default=MAX_LEN,
			  help='maximum length of fragmented message')
def main(max_len):
    with open('source.html', 'r', encoding='utf-8') as f:
        source = f.read()
        for fragment in split_message(source, max_len):
            print(f'==={len(fragment)}===')
            print(fragment)
            print("===")

if __name__ == '__main__':
    main()