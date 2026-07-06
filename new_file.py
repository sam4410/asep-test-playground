from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from slugify import slugify
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workspaces.db'
db = SQLAlchemy(app)

class Workspace(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    owner = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'owner': self.owner
        }

@app.route('/api/v1/workspaces', methods=['POST'])
def create_workspace():
    data = request.json
    name = data.get('name')
    owner = data.get('owner')
    
    if not name or not owner:
        return jsonify({'message': 'Name and owner are required fields.'}), 400

    slug = slugify(name)

    # Ensure slug is unique
    while Workspace.query.filter_by(slug=slug).first():
        slug = f"{slug}-{uuid.uuid4().hex[:6]}"

    workspace = Workspace(id=str(uuid.uuid4()), name=name, slug=slug, owner=owner)
    db.session.add(workspace)
    db.session.commit()

    return jsonify(workspace.to_dict()), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=False)