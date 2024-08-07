class UsersController < ApplicationController
  def index
  end


  private
  def user_params
    params.require(:user).permit(:name,:email,:admin,:encrypted_password)
  end
  def create
    @user = User.new(user_params)
  end
end
