#!/usr/bin/env python3
"""
Coder CLI - Project scaffolding and codegen using LLM agents
"""

import click
import os
from agents.runner import run_agent
from pathlib import Path

@click.group()
@click.version_option(version='1.0.0')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, verbose):
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    if verbose:
        click.echo("Verbose mode enabled")

@cli.command()
@click.argument("idea", required=False)
@click.option("--file", "-f", type=click.Path(exists=True), help="Markdown/text file with project brief")
@click.option("--format", type=click.Choice(["json", "markdown"]), default="json")
@click.option("--mvp", is_flag=True, help="Focus on MVP delivery (default behavior)")
@click.pass_context
def spec(ctx, idea, file, format, mvp):
    "Generate a project spec from a brief or file"
    if file:
        input_str = Path(file).read_text(encoding="utf-8")
        click.echo(f"📄 Loaded project brief from {file}")
    elif idea:
        input_str = f"{idea}\n\nFormat: {format.upper()}\nFocus on MVP: {mvp}"
    else:
        raise click.UsageError("Must provide either --file or an idea argument.")

    click.echo("🔧 Running SpecAgent...")
    result = run_agent("SpecAgent", input_str)

    output_path = Path("output/spec." + ("json" if format == "json" else "md"))
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(result, encoding="utf-8")
    click.echo(f"✅ Spec saved to {output_path}")


@cli.command()
@click.option("--file", "-f", type=click.Path(exists=True), required=True, help="Path to spec.json file")
@click.pass_context
def scaffold(ctx, file):
    """
    Generate project folder and file structure from a spec.json
    """
    from agents.runner import run_agent
    input_str = Path(file).read_text(encoding="utf-8")

    click.echo("🧱 Running ScaffoldAgent...")
    result = run_agent("ScaffoldAgent", input_str)

    output_path = Path("output/scaffold.md")
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(result, encoding="utf-8")
    click.echo(f"✅ Scaffold saved to {output_path}")

@cli.command()
@click.option("--file", "-f", type=click.Path(exists=True), required=True, help="Path to scaffold.md")
@click.option("--outdir", "-o", type=click.Path(), default="output/CheckInTV", help="Target folder for project")
@click.pass_context
def parse_scaffold(ctx, file, outdir):
    """
    Extract and create real file structure from scaffold.md
    """
    import re
    from pathlib import Path

    text = Path(file).read_text(encoding="utf-8")
    out_path = Path(outdir)
    out_path.mkdir(parents=True, exist_ok=True)

    pattern = re.compile(r"\*\*(.+?)\*\*\n```(\w+)?\n(.*?)\n```", re.DOTALL)
    created = []

    for match in pattern.finditer(text):
        filepath, _, content = match.groups()
        fullpath = out_path / filepath.strip()
        fullpath.parent.mkdir(parents=True, exist_ok=True)
        fullpath.write_text(content.strip(), encoding="utf-8")
        created.append(str(fullpath.relative_to(out_path)))

    manifest = out_path / "FILES.txt"
    manifest.write_text("\n".join(created), encoding="utf-8")
    click.echo(f"✅ Parsed and saved {len(created)} files to {outdir}")


@cli.command()
@click.option("--task", "-t", required=True, help="Describe what DevAgent should do.")
@click.option("--context", "-c", type=click.Path(exists=True), help="Optional folder or spec file for context")
@click.option("--output", "-o", type=click.Path(), default="output/dev_output.md", help="Where to save result")
@click.pass_context
def dev(ctx, task, context, output):
    """
    Run DevAgent on a specific task using optional context files
    """
    from agents.runner import run_agent
    from pathlib import Path

    ctx_input = f"\n\nProject context:\n"

    if context:
        context_path = Path(context)
        if context_path.is_dir():
            for file in sorted(context_path.glob("**/*")):
                if file.is_file() and file.suffix in [".html", ".js", ".css", ".json", ".md"]:
                    content = file.read_text(encoding="utf-8")
                    ctx_input += f"\n\nFile: {file.name}\n```\n{content[:2000]}\n```"  # truncate long files
        else:
            content = context_path.read_text(encoding="utf-8")
            ctx_input += f"\n\n{content[:3000]}"

    full_input = f"Task: {task.strip()}\n{ctx_input}"

    click.echo("🧠 Running DevAgent...")
    result = run_agent("DevAgent", full_input)

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(result.strip(), encoding="utf-8")
    click.echo(f"✅ Output saved to {output}")

@cli.command()
@click.option("--file", "-f", type=click.Path(exists=True), required=True, help="Path to dev_output.md file")
@click.option("--outdir", "-o", type=click.Path(), default="output/dev", help="Directory to extract files into")
def parse_dev(file, outdir):
    """
    Parses DevAgent markdown output into real files on disk
    """
    import re
    from pathlib import Path

    text = Path(file).read_text(encoding="utf-8")
    out_path = Path(outdir)
    out_path.mkdir(parents=True, exist_ok=True)

    pattern = re.compile(r"Filename:\s*`(.+?)`\s*```(?:\w+)?\n(.*?)\n```", re.DOTALL)
    created = []

    for match in pattern.finditer(text):
        rel_path, content = match.groups()
        full_path = out_path / rel_path.strip()
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content.strip(), encoding="utf-8")
        created.append(str(full_path.relative_to(out_path)))

    manifest = out_path / "FILES.txt"
    manifest.write_text("\n".join(created), encoding="utf-8")
    click.echo(f"✅ Extracted {len(created)} files to: {outdir}")

if __name__ == "__main__":
    cli()