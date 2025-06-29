"""Migración inicial limpia

Revision ID: e12904bf0de2
Revises: 
Create Date: 2025-06-17 19:55:49.426745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e12904bf0de2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('desempeno_modelo',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=False),
    sa.Column('formato', sa.String(), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('precision', sa.Float(), nullable=True),
    sa.Column('recall', sa.Float(), nullable=True),
    sa.Column('dataset', sa.String(), nullable=True),
    sa.Column('fecha_entrenamiento', sa.DateTime(), nullable=True),
    sa.Column('optimizado', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('telefono', sa.String(), nullable=False),
    sa.Column('registro', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('imagenes',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('nombre_imagen', sa.String(), nullable=False),
    sa.Column('ruta', sa.String(), nullable=False),
    sa.Column('usuario_id', sa.UUID(), nullable=True),
    sa.Column('fecha', sa.DateTime(), nullable=False),
    sa.Column('modelo_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['modelo_id'], ['desempeno_modelo.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('clasificacion_materiales',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('nombre_material', sa.String(), nullable=False),
    sa.Column('tipo_material', sa.String(), nullable=False),
    sa.Column('renovable', sa.Boolean(), nullable=True),
    sa.Column('reciclable', sa.Boolean(), nullable=True),
    sa.Column('confianza', sa.Float(), nullable=False),
    sa.Column('impacto_ambiental', sa.String(), nullable=True),
    sa.Column('imagen', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['imagen'], ['imagenes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clasificacion_materiales')
    op.drop_table('imagenes')
    op.drop_table('usuarios')
    op.drop_table('desempeno_modelo')
    # ### end Alembic commands ###
