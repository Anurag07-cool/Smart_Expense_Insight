from database.db import db
from datetime import datetime

class ReportModel(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    month = db.Column(db.String(10), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "_id": self.id,
            "user_id": self.user_id,
            "month": self.month,
            "year": self.year,
            "filename": self.filename,
            "created_at": self.created_at
        }

    @staticmethod
    def add_report(user_id, month, year, filename):
        report = ReportModel(
            user_id=int(user_id),
            month=month,
            year=year,
            filename=filename
        )
        db.session.add(report)
        db.session.commit()
        return str(report.id)

    @staticmethod
    def get_reports_by_user(user_id):
        reports = ReportModel.query.filter_by(user_id=int(user_id)).order_by(ReportModel.created_at.desc()).all()
        return [r.to_dict() for r in reports]
