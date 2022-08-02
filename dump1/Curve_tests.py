from dpp import formulae_x_y, formulae_y_x

for reserve_a, reserve_b, a, fee_bps, x, y in [
  [13247022.86, 45455154.14, 50, 15, 1, 1.0420],
  [13247022.86, 45455154.14, 50, 15, 30000000, 30032918.92],
  #...
]:
  assert formulae_x_y(reserve_a, reserve_b, a, fee_bps, y) == x


for reserve_a, reserve_b, a, fee_bps, x, y in [
  [13247022.86, 45455154.14, 50, 15, 1, 0.9569],
  [13247022.86, 45455154.14, 50, 15, 30000000, 2835113.25],
  #...
]:
  assert formulae_y_x(reserve_a, reserve_b, a, fee_bps, x) == y






