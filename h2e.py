#!/usr/bin/env python3
"""
Hashnode to 11ty Converter (h2e)

A Python CLI tool for converting Hashnode blog exports to 11ty-compatible format.
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from converter import HashNodeParser, HashNodeEnricher, ContentTransformer, ImageHandler

console = Console()

# Load environment variables
load_dotenv()


@click.command()
@click.argument('export_file', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path), default=Path('./output'),
              help='Output directory for generated files')
@click.option('--limit', '-l', type=int, help='Limit number of posts to process (for testing)')
@click.option('--skip-enrichment', is_flag=True, 
              help='Skip API enrichment (tags will show as IDs)')
@click.option('--skip-images', is_flag=True,
              help='Skip image downloads (use remote URLs)')
@click.option('--api-key', type=str, help='Hashnode API key (overrides HASHNODE_API_KEY env var)')
@click.option('--dry-run', is_flag=True, help='Show what would be done without writing files')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
def cli(export_file: Path, output: Path, limit: Optional[int], skip_enrichment: bool,
        skip_images: bool, api_key: Optional[str], dry_run: bool, verbose: bool):
    """
    Convert Hashnode blog export to 11ty-compatible format.
    
    EXPORT_FILE: Path to the Hashnode JSON export file
    """
    
    # Set up console logging
    if verbose:
        console.print(f"[blue]Export file: {export_file}[/blue]")
        console.print(f"[blue]Output directory: {output}[/blue]")
        if limit:
            console.print(f"[blue]Limit: {limit} posts[/blue]")
        console.print(f"[blue]Skip enrichment: {skip_enrichment}[/blue]")
        console.print(f"[blue]Skip images: {skip_images}[/blue]")
        console.print(f"[blue]Dry run: {dry_run}[/blue]")
        console.print()
    
    try:
        converter = HashNodeConverter(
            api_key=api_key,
            skip_enrichment=skip_enrichment,
            skip_images=skip_images,
            verbose=verbose
        )
        
        converter.convert(
            export_file=export_file,
            output_dir=output,
            limit=limit,
            dry_run=dry_run
        )
        
    except KeyboardInterrupt:
        console.print("\n[red]Conversion interrupted by user[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Conversion failed: {e}[/red]")
        if verbose:
            console.print_exception()
        sys.exit(1)


class HashNodeConverter:
    """Main converter orchestrating the conversion process."""
    
    def __init__(self, api_key: Optional[str] = None, skip_enrichment: bool = False,
                 skip_images: bool = False, verbose: bool = False):
        """Initialize converter with options."""
        self.api_key = api_key or os.getenv('HASHNODE_API_KEY')
        self.skip_enrichment = skip_enrichment
        self.skip_images = skip_images
        self.verbose = verbose
        
        # Initialize components
        self.enricher = HashNodeEnricher(api_key=self.api_key)
        self.transformer = ContentTransformer()
        self.image_handler = ImageHandler()
        
    def convert(self, export_file: Path, output_dir: Path, limit: Optional[int] = None,
                dry_run: bool = False) -> None:
        """Main conversion process."""
        
        console.print("🚀 [bold blue]Starting Hashnode to 11ty conversion...[/bold blue]\n")
        
        # Phase 1: Parse export file
        console.print("📋 [blue]Phase 1: Parsing export file...[/blue]")
        parser = HashNodeParser(str(export_file))
        parser.load_export()
        
        summary = parser.get_summary()
        posts = parser.get_posts(limit=limit)
        
        console.print(f"   Found {summary['total_posts']} posts from publication: {summary['publication_title']}")
        if limit and limit < summary['total_posts']:
            console.print(f"   [yellow]Limited to {limit} posts for testing[/yellow]")
        console.print()
        
        # Phase 2: Enrich data
        if self.skip_enrichment:
            console.print("⏭️  [yellow]Phase 2: Skipping API enrichment (--skip-enrichment flag)...[/yellow]")
            enriched_data = self.enricher.create_fallback_enrichment(posts)
        elif not self.enricher.can_enrich():
            console.print("⏭️  [yellow]Phase 2: Skipping API enrichment (no API key)...[/yellow]")
            enriched_data = self.enricher.create_fallback_enrichment(posts)
        else:
            console.print("🔍 [blue]Phase 2: Enriching data from Hashnode API...[/blue]")
            post_ids = [post['_id'] for post in posts]
            enriched_data = self.enricher.enrich_posts(post_ids)
            
            # Also enrich publication series if we have publication info
            pub_info = parser.get_publication_info()
            if pub_info.get('_id'):
                series_data = self.enricher.enrich_publication_series(pub_info['_id'])
                if self.verbose and series_data:
                    console.print(f"   Found {len(series_data)} series in publication")
                    
        console.print()
        
        # Phase 3: Transform content
        console.print("📝 [blue]Phase 3: Transforming content to 11ty format...[/blue]")
        transformed_posts = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            task = progress.add_task("Transforming posts", total=len(posts))
            
            for post in posts:
                post_id = post['_id']
                enriched_post = enriched_data.get(post_id, {})
                
                if not enriched_post:
                    console.print(f"[yellow]Warning: No enriched data for post {post_id}[/yellow]")
                    continue
                    
                transformed_post = self.transformer.transform_post(post, enriched_post)
                transformed_posts.append(transformed_post)
                
                progress.advance(task)
                
        console.print(f"   Transformed {len(transformed_posts)} posts")
        console.print()
        
        # Phase 4: Process images
        if self.skip_images:
            console.print("⏭️  [yellow]Phase 4: Skipping image downloads...[/yellow]")
        else:
            console.print("🖼️  [blue]Phase 4: Processing images...[/blue]")
            self.image_handler.base_image_dir = output_dir / "images"
            transformed_posts = self.image_handler.batch_download_images(transformed_posts)
            
            # Show image statistics
            stats = self.image_handler.get_image_stats()
            console.print(f"   Downloaded images for {stats['total_posts']} posts")
            console.print(f"   Total images: {stats['total_images']} ({stats['total_size_mb']} MB)")
            
        console.print()
        
        # Phase 5: Generate files
        if dry_run:
            console.print("🔍 [yellow]Phase 5: Dry run - showing what would be generated...[/yellow]")
            self._show_dry_run_output(transformed_posts, output_dir)
        else:
            console.print("📄 [blue]Phase 5: Generating 11ty files...[/blue]")
            self._generate_files(transformed_posts, output_dir)
            
        console.print()
        console.print("✅ [bold green]Conversion completed successfully![/bold green]")
        
        # Show summary
        self._show_summary(transformed_posts, output_dir, dry_run)
        
    def _generate_files(self, posts: list, output_dir: Path) -> None:
        """Generate all output files."""
        # Create directory structure
        posts_dir = output_dir / "content" / "posts"
        data_dir = output_dir / "_data"
        
        for dir_path in [posts_dir, data_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # Generate post files
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            task = progress.add_task("Generating post files", total=len(posts))
            
            for post in posts:
                post_file = posts_dir / f"{post['slug']}.md"
                content = self.transformer.generate_markdown_file(post)
                
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                progress.advance(task)
                
        # Generate collection config
        posts_json = posts_dir / "posts.json"
        with open(posts_json, 'w', encoding='utf-8') as f:
            json.dump({"layout": "post"}, f, indent=2)
            
        # Generate metadata files
        self._generate_metadata(posts, data_dir)
        
        console.print(f"   Generated {len(posts)} post files")
        console.print(f"   Generated metadata files")
        
    def _generate_metadata(self, posts: list, data_dir: Path) -> None:
        """Generate metadata files for 11ty."""
        # Collect tags and series
        all_tags = {}
        all_series = {}
        
        for post in posts:
            # Process tags
            for tag_name in post.get('tags', []):
                tag_slug = self._slugify(tag_name)
                if tag_slug not in all_tags:
                    all_tags[tag_slug] = {
                        'name': tag_name,
                        'slug': tag_slug,
                        'count': 0
                    }
                all_tags[tag_slug]['count'] += 1
                
            # Process series
            if post.get('series'):
                series_name = post['series']
                series_slug = self._slugify(series_name)
                if series_slug not in all_series:
                    all_series[series_slug] = {
                        'name': series_name,
                        'slug': series_slug,
                        'description': '',
                        'count': 0
                    }
                all_series[series_slug]['count'] += 1
                
        # Write tags file
        tags_file = data_dir / "allTags.json"
        with open(tags_file, 'w', encoding='utf-8') as f:
            json.dump(all_tags, f, indent=2)
            
        # Write series file
        series_file = data_dir / "allSeries.json"
        with open(series_file, 'w', encoding='utf-8') as f:
            json.dump(all_series, f, indent=2)
            
        # Write basic metadata
        metadata = {
            'title': 'My Blog',
            'description': 'Migrated from Hashnode using h2e',
            'url': 'https://example.com',
            'author': {
                'name': 'Your Name',
                'email': 'your.email@example.com'
            },
            'totalPosts': len(posts),
            'totalTags': len(all_tags),
            'totalSeries': len(all_series),
            'generatedAt': '2024-01-01T00:00:00.000Z'
        }
        
        metadata_file = data_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
            
    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        import re
        slug = text.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
        
    def _show_dry_run_output(self, posts: list, output_dir: Path) -> None:
        """Show what would be generated in dry run mode."""
        console.print(f"   Would create {len(posts)} post files in: {output_dir}/content/posts/")
        console.print(f"   Would create metadata files in: {output_dir}/_data/")
        
        if posts:
            console.print("\n   Sample posts that would be generated:")
            for i, post in enumerate(posts[:3]):
                console.print(f"   - {post['slug']}.md")
                if i == 2 and len(posts) > 3:
                    console.print(f"   ... and {len(posts) - 3} more")
                    break
                    
    def _show_summary(self, posts: list, output_dir: Path, dry_run: bool) -> None:
        """Show final summary."""
        console.print("\n📈 [bold blue]Conversion Summary:[/bold blue]")
        console.print(f"   Total posts processed: {len(posts)}")
        
        # Count posts with various features
        posts_with_tags = len([p for p in posts if p.get('tags')])
        posts_with_series = len([p for p in posts if p.get('series')])
        posts_with_images = len([p for p in posts if p.get('coverImage')])
        
        console.print(f"   Posts with tags: {posts_with_tags}")
        console.print(f"   Posts with series: {posts_with_series}")
        console.print(f"   Posts with cover images: {posts_with_images}")
        
        if not dry_run:
            console.print(f"\n🎉 [bold green]Files generated in: {output_dir}[/bold green]")
            console.print("   Ready for 11ty build!")


if __name__ == '__main__':
    cli()