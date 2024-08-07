Rails.application.routes.draw do
  get 'racers_page/index'
  resources :reservations
  resources :races
  get 'home/index'
  get 'users' ,to: 'users#index'
  root 'home#index'
  devise_for :users
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Defines the root path route ("/")
  # root "articles#index"
end
