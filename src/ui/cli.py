import click
from src.core.scanner import scan_for_pdfs


@click.command()
@click.argument('path', type=click.Path(exists=True))
def main(path):
    """Scan the given PATH for PDF files and list them in order of last modified."""
    click.echo(f"Scanning {path} for PDF files...")
    pdf_files = scan_for_pdfs(path)

    if not pdf_files:
        click.echo("No PDF files found.")
        return

    click.echo(f"Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        click.echo(f"{pdf['path']} - Last modified: {pdf['modified']}")


if __name__ == '__main__':
    main()
