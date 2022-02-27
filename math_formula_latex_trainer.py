from app import app, db
from app.models import User, Exercise, Lesson, UserLessonExerciseProgress

@app.shell_context_processor
def make_shell_context():
    return {"db": db,
            "User": User,
            "Exercise": Exercise,
            "Lesson": Lesson,
            "UserLessonExerciseProgress": UserLessonExerciseProgress}
