// Part of measurement-kit <https://measurement-kit.github.io/>.
// Measurement-kit is free software under the BSD license. See AUTHORS
// and LICENSE for more information on the copying conditions.
#ifndef MEASUREMENT_KIT_COMMON_NON_COPYABLE_HPP
#define MEASUREMENT_KIT_COMMON_NON_COPYABLE_HPP

namespace mk {

/// \brief `NonCopyable` makes a derived class non-copyable. You typically need
/// to make non-copyable classes that manage the lifecycle of pointers.
///
/// \since v0.1.0.
class NonCopyable {
  public:
    NonCopyable(const NonCopyable &) = delete;
    NonCopyable &operator=(const NonCopyable &) = delete;
    NonCopyable(NonCopyable &) = delete;
    NonCopyable &operator=(NonCopyable &) = delete;
    NonCopyable() {}
};

} // namespace mk
#endif
