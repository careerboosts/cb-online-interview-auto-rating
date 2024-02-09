from pydantic.types import Json

def project_helper(project) -> dict:
    project['_id'] = str(project['_id'])
    return project
