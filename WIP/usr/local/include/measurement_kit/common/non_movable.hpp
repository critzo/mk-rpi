// Part of measurement-kit <https://measurement-kit.github.io/>.
// Measurement-kit is free software under the BSD license. See AUTHORS
// and LICENSE for more information on the copying conditions.
#ifndef MEASUREMENT_KIT_COMMON_NON_MOVABLE_HPP
#define MEASUREMENT_KIT_COMMON_NON_MOVABLE_HPP

namespace mk {

/// \brief `NonMovable` makes a derived class non-movable. You typically need to
/// make non-movable classes that manage the lifecycle of pointers.
///
/// \since v0.1.0.
class NonMovable {
  public:
    NonMovable(NonMovable &&) = delete;
    NonMovable &operator=(NonMovable &&) = delete;
    NonMovable() {}
};

} // namespace mk
#endif
