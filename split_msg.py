import click
from html_fragmentor import split_message
from html_fragmentor import MAX_LEN

@click.command()
@click.option('--max-len', default=MAX_LEN,
			  help='maximum length of fragmented message')
@click.argument('filename')
def main(max_len, filename):
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
        number = 0
        for fragment in split_message(source, max_len):
            number += 1
            fragmen_length = len(fragment)
            print(f'fragment #{number}: {fragmen_length} chars.')
            print(fragment)

if __name__ == '__main__':
    main()