class AddNameToRaces < ActiveRecord::Migration[7.0]
  def change
    add_column :races, :name, :string
  end
end
