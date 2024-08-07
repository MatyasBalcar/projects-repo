module HomeHelper
  def admin?
    current_user&.admin
  end
  def signed_in_as_admin?(i)
    if i
      'admin'
    else
      'user'
    end
  end
end
