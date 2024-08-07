class AddInfoToRaces < ActiveRecord::Migration[7.0]
  def change
    add_column :races, :time, :integer
    add_column :races, :driver, :string
    add_column :races, :race_number, :integer
    add_column :races, :weather, :string
  end
end
