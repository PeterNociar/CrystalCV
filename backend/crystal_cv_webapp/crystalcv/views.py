from crystalcv import auth
from crystalcv.exceptions import UserAlreadyExists
from crystalcv.models.models import Company, CompanyModel, User, UserModel


def register(username, password):
    if UserModel.get_one_by_keys(keys={'username': username}):
        raise UserAlreadyExists()
    user = User({'username': username, 'password': password})
    user.save()
    return user


def get_companies():
    user = auth.get_current_user()
    companies = CompanyModel.get_list(keys={'user_id': user.id})
    result = []
    for comp in companies:
        result.append(Company.from_orm(comp))

    return result


def add_company(user):
    pass


def update_company(user):
    pass


def delete_company(user):
    pass


def add_project(user, company_id):
    pass


def update_project(user, company_id):
    pass


def delete_project(user, company_id):
    pass


def get_skills(user):
    pass


def add_skill(user):
    pass


def update_skill(user):
    pass


def delete_skill(user):
    pass
