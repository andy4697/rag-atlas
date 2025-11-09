"""Initial database schema

Revision ID: c4e02a7259e5
Revises: 
Create Date: 2025-11-06 07:09:18.448134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4e02a7259e5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create authors table
    op.create_table(
        'authors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('affiliation', sa.String(length=500), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('orcid', sa.String(length=19), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_author_name', 'authors', ['name'])
    op.create_index('idx_author_orcid', 'authors', ['orcid'])
    op.create_index(op.f('ix_authors_id'), 'authors', ['id'])

    # Create categories table
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('parent_category', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index('idx_category_code', 'categories', ['code'])
    op.create_index('idx_category_parent', 'categories', ['parent_category'])
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'])

    # Create papers table
    op.create_table(
        'papers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('arxiv_id', sa.String(length=20), nullable=True),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('abstract', sa.Text(), nullable=False),
        sa.Column('published_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('pdf_url', sa.String(length=500), nullable=True),
        sa.Column('pdf_path', sa.String(length=500), nullable=True),
        sa.Column('full_text', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', name='paperstatus'), nullable=False),
        sa.Column('processing_metadata', sa.JSON(), nullable=True),
        sa.Column('citation_count', sa.Integer(), nullable=True),
        sa.Column('download_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('arxiv_id')
    )
    op.create_index('idx_paper_arxiv_id', 'papers', ['arxiv_id'])
    op.create_index('idx_paper_published_date', 'papers', ['published_date'])
    op.create_index('idx_paper_status', 'papers', ['status'])
    op.create_index(op.f('ix_papers_id'), 'papers', ['id'])
    op.create_index(op.f('ix_papers_title'), 'papers', ['title'])

    # Create job_descriptions table
    op.create_table(
        'job_descriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('company', sa.String(length=200), nullable=False),
        sa.Column('location', sa.String(length=100), nullable=True),
        sa.Column('employment_type', sa.String(length=50), nullable=True),
        sa.Column('experience_level', sa.Enum('ENTRY', 'JUNIOR', 'MID', 'SENIOR', 'EXECUTIVE', name='experiencelevel'), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('requirements', sa.JSON(), nullable=True),
        sa.Column('preferred_qualifications', sa.JSON(), nullable=True),
        sa.Column('responsibilities', sa.JSON(), nullable=True),
        sa.Column('required_skills', sa.JSON(), nullable=True),
        sa.Column('preferred_skills', sa.JSON(), nullable=True),
        sa.Column('keywords', sa.JSON(), nullable=True),
        sa.Column('salary_range', sa.String(length=100), nullable=True),
        sa.Column('benefits', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_job_company', 'job_descriptions', ['company'])
    op.create_index('idx_job_created_at', 'job_descriptions', ['created_at'])
    op.create_index('idx_job_experience_level', 'job_descriptions', ['experience_level'])
    op.create_index('idx_job_title', 'job_descriptions', ['title'])
    op.create_index(op.f('ix_job_descriptions_id'), 'job_descriptions', ['id'])

    # Create resumes table
    op.create_table(
        'resumes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=100), nullable=True),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=500), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('file_type', sa.String(length=20), nullable=False),
        sa.Column('original_text', sa.Text(), nullable=True),
        sa.Column('parsed_data', sa.JSON(), nullable=True),
        sa.Column('analysis_results', sa.JSON(), nullable=True),
        sa.Column('enhancement_suggestions', sa.JSON(), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', name='resumestatus'), nullable=False),
        sa.Column('processing_metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_resume_created_at', 'resumes', ['created_at'])
    op.create_index('idx_resume_status', 'resumes', ['status'])
    op.create_index('idx_resume_user_id', 'resumes', ['user_id'])
    op.create_index(op.f('ix_resumes_id'), 'resumes', ['id'])

    # Create chunks table
    op.create_table(
        'chunks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('paper_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('section_title', sa.String(length=200), nullable=True),
        sa.Column('section_type', sa.String(length=50), nullable=True),
        sa.Column('embedding', sa.JSON(), nullable=True),
        sa.Column('embedding_model', sa.String(length=100), nullable=True),
        sa.Column('token_count', sa.Integer(), nullable=True),
        sa.Column('char_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_chunk_paper_id', 'chunks', ['paper_id'])
    op.create_index('idx_chunk_paper_index', 'chunks', ['paper_id', 'chunk_index'])
    op.create_index('idx_chunk_section_type', 'chunks', ['section_type'])
    op.create_index(op.f('ix_chunks_id'), 'chunks', ['id'])

    # Create job_matches table
    op.create_table(
        'job_matches',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('job_id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('overall_match_score', sa.Float(), nullable=False),
        sa.Column('skill_match_score', sa.Float(), nullable=False),
        sa.Column('experience_match_score', sa.Float(), nullable=False),
        sa.Column('matching_skills', sa.JSON(), nullable=True),
        sa.Column('missing_skills', sa.JSON(), nullable=True),
        sa.Column('skill_gaps', sa.JSON(), nullable=True),
        sa.Column('recommendations', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['job_id'], ['job_descriptions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('job_id', 'resume_id', name='uq_job_resume_match')
    )
    op.create_index('idx_job_match_job_id', 'job_matches', ['job_id'])
    op.create_index('idx_job_match_overall_score', 'job_matches', ['overall_match_score'])
    op.create_index('idx_job_match_resume_id', 'job_matches', ['resume_id'])
    op.create_index(op.f('ix_job_matches_id'), 'job_matches', ['id'])

    # Create paper_authors table
    op.create_table(
        'paper_authors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('paper_id', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('author_order', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('paper_id', 'author_id', name='uq_paper_author')
    )
    op.create_index('idx_paper_author_author_id', 'paper_authors', ['author_id'])
    op.create_index('idx_paper_author_paper_id', 'paper_authors', ['paper_id'])

    # Create paper_categories table
    op.create_table(
        'paper_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('paper_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('paper_id', 'category_id', name='uq_paper_category')
    )
    op.create_index('idx_paper_category_category_id', 'paper_categories', ['category_id'])
    op.create_index('idx_paper_category_paper_id', 'paper_categories', ['paper_id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop tables in reverse order due to foreign key constraints
    op.drop_table('paper_categories')
    op.drop_table('paper_authors')
    op.drop_table('job_matches')
    op.drop_table('chunks')
    op.drop_table('resumes')
    op.drop_table('job_descriptions')
    op.drop_table('papers')
    op.drop_table('categories')
    op.drop_table('authors')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS paperstatus')
    op.execute('DROP TYPE IF EXISTS resumestatus')
    op.execute('DROP TYPE IF EXISTS experiencelevel')
